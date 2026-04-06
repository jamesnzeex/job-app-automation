"""
Job Application Automation API
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from ..models.database import get_db
from ..models.models import Application, ApplicationStatus, JobPlatform, Interview

app = FastAPI(
    title="Job Application Automation API",
    description="Backend API for tracking job applications and automating the job search process",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Application Endpoints ==============

@app.get("/api/applications")
def list_applications(
    status: Optional[str] = None,
    company: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all applications with optional filters"""
    query = db.query(Application)
    
    if status:
        query = query.filter(Application.status == status)
    if company:
        query = query.filter(Application.company.ilike(f"%{company}%"))
    
    applications = query.all()
    
    return [
        {
            "id": app.id,
            "company": app.company,
            "position": app.position,
            "status": app.status.value,
            "job_url": app.job_url,
            "platform": app.platform.value if app.platform else None,
            "posted_date": app.posted_date.isoformat() if app.posted_date else None,
            "applied_date": app.applied_date.isoformat() if app.applied_date else None,
            "location": app.location,
            "remote": app.remote,
            "notes": app.notes,
            "created_at": app.created_at.isoformat(),
        }
        for app in applications
    ]


@app.post("/api/applications")
def create_application(application: dict, db: Session = Depends(get_db)):
    """Create a new application"""
    db_app = Application(
        company=application["company"],
        position=application["position"],
        job_url=application.get("job_url"),
        platform=JobPlatform[application.get("platform", "OTHER").upper()] if application.get("platform") else None,
        status=ApplicationStatus[application.get("status", "PENDING").upper()] if application.get("status") else ApplicationStatus.PENDING,
        posted_date=datetime.fromisoformat(application["posted_date"]) if application.get("posted_date") else None,
        applied_date=datetime.fromisoformat(application["applied_date"]) if application.get("applied_date") else None,
        salary_min=application.get("salary_min"),
        salary_max=application.get("salary_max"),
        currency=application.get("currency", "USD"),
        location=application.get("location"),
        remote=application.get("remote", False),
        resume_path=application.get("resume_path"),
        cover_letter=application.get("cover_letter"),
        requirements=application.get("requirements"),
        skills_matched=application.get("skills_matched"),
        notes=application.get("notes"),
        recruiter_link=application.get("recruiter_link"),
        hiring_manager_link=application.get("hiring_manager_link"),
    )
    
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    return {
        "id": db_app.id,
        "company": db_app.company,
        "position": db_app.position,
        "status": db_app.status.value,
    }


@app.get("/api/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application"""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return {
        "id": app.id,
        "company": app.company,
        "position": app.position,
        "status": app.status.value,
        "job_url": app.job_url,
        "platform": app.platform.value if app.platform else None,
        "posted_date": app.posted_date.isoformat() if app.posted_date else None,
        "applied_date": app.applied_date.isoformat() if app.applied_date else None,
        "salary_min": app.salary_min,
        "salary_max": app.salary_max,
        "currency": app.currency,
        "location": app.location,
        "remote": app.remote,
        "resume_path": app.resume_path,
        "cover_letter": app.cover_letter,
        "requirements": app.requirements,
        "skills_matched": app.skills_matched,
        "notes": app.notes,
        "follow_up_required": app.follow_up_required,
        "follow_up_date": app.follow_up_date.isoformat() if app.follow_up_date else None,
        "recruiter_link": app.recruiter_link,
        "hiring_manager_link": app.hiring_manager_link,
        "created_at": app.created_at.isoformat(),
    }


@app.put("/api/applications/{application_id}")
def update_application(application_id: int, application: dict, db: Session = Depends(get_db)):
    """Update an application"""
    db_app = db.query(Application).filter(Application.id == application_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields
    for field, value in application.items():
        if hasattr(db_app, field) and value is not None:
            setattr(db_app, field, value)
    
    db.commit()
    db.refresh(db_app)
    
    return {"message": "Application updated", "id": db_app.id}


@app.delete("/api/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete an application"""
    db_app = db.query(Application).filter(Application.id == application_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    db.delete(db_app)
    db.commit()
    
    return {"message": "Application deleted", "id": application_id}


# ============== Analytics Endpoints ==============

@app.get("/api/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    """Get overview analytics"""
    total = db.query(Application).count()
    by_status = db.query(Application.status).group_by(Application.status).count()
    
    return {
        "total_applications": total,
        "by_status": dict(by_status),
    }


# ============== Interview Endpoints ==============

@app.get("/api/interviews")
def list_interviews(db: Session = Depends(get_db)):
    """List all interviews"""
    interviews = db.query(Interview).all()
    
    return [
        {
            "id": interview.id,
            "application_id": interview.application_id,
            "company": interview.company,
            "position": interview.position,
            "type": interview.type,
            "scheduled_at": interview.scheduled_at.isoformat() if interview.scheduled_at else None,
            "status": interview.status,
            "created_at": interview.created_at.isoformat(),
        }
        for interview in interviews
    ]


@app.post("/api/interviews")
def create_interview(interview: dict, db: Session = Depends(get_db)):
    """Create a new interview"""
    db_interview = Interview(
        application_id=interview["application_id"],
        company=interview["company"],
        position=interview["position"],
        type=interview["type"],
        scheduled_at=datetime.fromisoformat(interview["scheduled_at"]) if interview.get("scheduled_at") else None,
        duration_minutes=interview.get("duration_minutes"),
        status=interview.get("status", "scheduled"),
        interviewer_names=interview.get("interviewer_names"),
        interviewer_links=interview.get("interviewer_links"),
        prep_notes=interview.get("prep_notes"),
    )
    
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    
    return db_interview


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
