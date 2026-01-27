from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from database import get_db
from models import ScrapingHistory

router = APIRouter()

class HistoryItem(BaseModel):
    id: int
    source_url: str
    site_name: str
    job_count: int
    scraped_at: str
    status: str
    
    class Config:
        from_attributes = True

@router.get("/history", response_model=List[HistoryItem])
async def get_history(
    site: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(ScrapingHistory)
    
    filters = []
    
    if site:
        filters.append(ScrapingHistory.site_name == site)
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            filters.append(ScrapingHistory.scraped_at >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            filters.append(ScrapingHistory.scraped_at <= end)
        except ValueError:
            pass
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.order_by(ScrapingHistory.scraped_at.desc())
    histories = query.offset(offset).limit(limit).all()
    
    return [
        HistoryItem(
            id=h.id,
            source_url=h.source_url,
            site_name=h.site_name,
            job_count=h.job_count,
            scraped_at=h.scraped_at.isoformat(),
            status=h.status
        )
        for h in histories
    ]

@router.get("/history/{history_id}", response_model=HistoryItem)
async def get_history_detail(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(ScrapingHistory).filter(ScrapingHistory.id == history_id).first()
    
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    
    return HistoryItem(
        id=history.id,
        source_url=history.source_url,
        site_name=history.site_name,
        job_count=history.job_count,
        scraped_at=history.scraped_at.isoformat(),
        status=history.status
    )
