from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from database import get_db
from models import ScrapingHistory, JobListing
from services.csharp_bridge import CSharpScraperBridge
from services.csv_generator import CSVGenerator
from services.file_manager import FileManager
import os
import logging
from urllib.parse import unquote

logger = logging.getLogger(__name__)

router = APIRouter()

class ScrapeRequest(BaseModel):
    url: str
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('URL is required')
        return v.strip()

class ScrapeResponse(BaseModel):
    job_count: int
    site_name: str
    source_url: str
    scraped_at: str
    csv_url: Optional[str] = None
    jobs: list

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_jobs(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info(f"=== Starting scrape request ===")
    logger.info(f"Request URL: {request.url}")
    
    try:
        url = request.url
        logger.info(f"Processing URL: {url}")
        
        bridge = CSharpScraperBridge()
        logger.info("CSharpScraperBridge initialized")
        
        result = await bridge.scrape(url)
        logger.info(f"Scraping completed. Job count: {result.get('jobCount', 0) if result else 0}")
        
        if not result:
            logger.error("No result returned from scraper")
            raise HTTPException(status_code=400, detail="Scraping failed: No result")
        
        if "error" in result:
            logger.error(f"Scraper returned error: {result['error']}")
            raise HTTPException(status_code=400, detail=result.get("error", "Scraping failed"))
        
        logger.info(f"Creating history entry...")
        history = ScrapingHistory(
            user_id=None,
            source_url=url,
            site_name=result.get("siteName", "unknown"),
            job_count=result.get("jobCount", 0),
            scraped_at=datetime.utcnow(),
            status="completed"
        )
        db.add(history)
        db.flush()
        logger.info(f"History entry created with ID: {history.id}")
        
        jobs = result.get("jobs", [])
        logger.info(f"Processing {len(jobs)} jobs...")
        
        for job_data in jobs:
            job = JobListing(
                history_id=history.id,
                company_name=job_data.get("companyName"),
                industry_type=job_data.get("industryType"),
                job_type=job_data.get("jobType"),
                employment_type=job_data.get("employmentType"),
                work_hours=job_data.get("workHours"),
                job_description=job_data.get("jobDescription"),
                salary=job_data.get("salary"),
                company_location=job_data.get("companyLocation"),
                work_location=job_data.get("workLocation"),
                benefits=job_data.get("benefits"),
                holidays=job_data.get("holidays"),
                requirements=job_data.get("requirements"),
                job_url=job_data.get("jobUrl")
            )
            db.add(job)
        
        db.commit()
        logger.info("Database commit successful")
        
        logger.info("Generating CSV...")
        csv_generator = CSVGenerator()
        csv_path = csv_generator.generate(history.id, jobs)
        logger.info(f"CSV generated at: {csv_path}")
        
        history.csv_path = csv_path
        db.commit()
        
        file_manager = FileManager()
        csv_url = file_manager.get_download_url(history.id)
        logger.info(f"CSV URL: {csv_url}")
        
        logger.info("=== Scrape request completed successfully ===")
        return ScrapeResponse(
            job_count=result.get("jobCount", 0),
            site_name=result.get("siteName", "unknown"),
            source_url=url,
            scraped_at=datetime.utcnow().isoformat(),
            csv_url=csv_url,
            jobs=jobs
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Exception in scrape_jobs: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{history_id}")
async def download_csv(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(ScrapingHistory).filter(ScrapingHistory.id == history_id).first()
    
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    
    if not history.csv_path or not os.path.exists(history.csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    return FileResponse(
        path=history.csv_path,
        filename=f"job-scraping-{history_id}.csv",
        media_type="text/csv"
    )
