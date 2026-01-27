from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scraping_histories = relationship("ScrapingHistory", back_populates="user")

class ScrapingHistory(Base):
    __tablename__ = "scraping_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_url = Column(Text, nullable=False)
    site_name = Column(String(100), nullable=False)
    job_count = Column(Integer, default=0)
    csv_path = Column(String(500))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="completed")
    error_message = Column(Text)
    
    user = relationship("User", back_populates="scraping_histories")
    jobs = relationship("JobListing", back_populates="history")

class JobListing(Base):
    __tablename__ = "job_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    history_id = Column(Integer, ForeignKey("scraping_histories.id"), nullable=False)
    company_name = Column(String(500))
    industry_type = Column(String(200))
    job_type = Column(String(500))
    employment_type = Column(String(100))
    work_hours = Column(Text)
    job_description = Column(Text)
    salary = Column(Text)
    company_location = Column(Text)
    work_location = Column(Text)
    benefits = Column(Text)
    holidays = Column(Text)
    requirements = Column(Text)
    job_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    history = relationship("ScrapingHistory", back_populates="jobs")
