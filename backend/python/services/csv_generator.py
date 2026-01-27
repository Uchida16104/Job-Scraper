import csv
import os
from typing import List, Dict, Any
from datetime import datetime
from config import settings

class CSVGenerator:
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate(self, history_id: int, jobs: List[Dict[Any, Any]]) -> str:
        filename = f"scraping_{history_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        headers = [
            "会社名 / Company Name",
            "業種 / Industry",
            "職種 / Job Type",
            "雇用形態 / Employment Type",
            "勤務時間 / Work Hours",
            "仕事内容 / Job Description",
            "給与 / Salary",
            "会社所在地 / Company Location",
            "勤務地 / Work Location",
            "福利厚生 / Benefits",
            "休日・休暇 / Holidays",
            "対象となる方 / Requirements",
            "求人URL / Job URL"
        ]
        
        with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            
            for job in jobs:
                row = [
                    job.get("companyName", ""),
                    job.get("industryType", ""),
                    job.get("jobType", ""),
                    job.get("employmentType", ""),
                    job.get("workHours", ""),
                    job.get("jobDescription", ""),
                    job.get("salary", ""),
                    job.get("companyLocation", ""),
                    job.get("workLocation", ""),
                    job.get("benefits", ""),
                    job.get("holidays", ""),
                    job.get("requirements", ""),
                    job.get("jobUrl", "")
                ]
                writer.writerow(row)
        
        return filepath
