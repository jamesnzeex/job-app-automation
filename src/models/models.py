"""
Database models for Job Application Automation
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.sqlite import ENUM

Base = declarative_base()


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    ACCEPTED = "accepted"


class JobPlatform(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    COMPANY_SITE = "company_site"
    OTHER = "other"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    job_url = Column(String(500), unique=True, nullable=True)
    platform = Column(SQLEnum(JobPlatform), default=JobPlatform.OTHER)
    
    # Status tracking
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.PENDING)
    
    # Dates
    posted_date = Column(DateTime, nullable=True)
    applied_date = Column(DateTime, nullable=True)
    last_contact_date = Column(DateTime, nullable=True)
    
    # Salary & location
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    location = Column(String(255), nullable=True)
    remote = Column(Boolean, default=False)
    
    # Application details
    resume_path = Column(String(500), nullable=True)
    cover_letter = Column(Text, nullable=True)
    cover_letter_template = Column(String(255), nullable=True)
    
    # Notes
    requirements = Column(Text, nullable=True)  # Key JD requirements
    skills_matched = Column(Text, nullable=True)  # Matched skills from resume
    notes = Column(Text, nullable=True)
    
    # Follow-up tracking
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    follow_up_sent = Column(Boolean, default=False)
    
    # Links
    recruiter_link = Column(String(500), nullable=True)
    hiring_manager_link = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Application({self.company}, {self.position}, {self.status})>"


class JobSource(Base):
    """Track where job postings came from for analytics"""
    __tablename__ = "job_sources"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(SQLEnum(JobPlatform), nullable=False)
    url = Column(String(500), unique=True, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)


class Interview(Base):
    """Track interview details"""
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=False)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    
    # Interview details
    type = Column(String(50), nullable=False)  # phone, technical, final, etc.
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    interviewer_names = Column(Text, nullable=True)
    interviewer_links = Column(Text, nullable=True)
    
    # Prep
    prep_notes = Column(Text, nullable=True)
    
    # Outcome
    outcome = Column(String(50), nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Contact(Base):
    """Track recruiters and hiring managers"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=True)  # Link to application if known
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)  # Recruiter, Hiring Manager, etc.
    email = Column(String(255), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Relationship tracking
    relationship_notes = Column(Text, nullable=True)
    last_contacted = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Note(Base):
    """Track notes about applications or companies"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=True)
    company = Column(String(255), nullable=True)
    
    # Note content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general, follow_up, interview_prep, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobSource(Base):
    """Track where job postings came from for analytics"""
    __tablename__ = "job_sources"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(SQLEnum(JobPlatform), nullable=False)
    url = Column(String(500), unique=True, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
