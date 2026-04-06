"""
Tests for database models
"""
import pytest
from src.models.database import init_db, get_db, SessionLocal
from src.models.models import Application, ApplicationStatus, JobPlatform, Interview

# Initialize test database
init_db()


class TestApplication:
    def test_create_application(self):
        """Test creating a new application"""
        from datetime import datetime
        db = SessionLocal()
        
        app = Application(
            company="TechCorp",
            position="ML Engineer",
            job_url="https://linkedin.com/jobs/123",
            platform=JobPlatform.LINKEDIN,
            status=ApplicationStatus.APPLIED,
            posted_date=datetime.now(),
            location="San Francisco, CA",
            remote=True,
            salary_min=150000,
            salary_max=200000,
        )
        
        db.add(app)
        db.commit()
        db.refresh(app)
        
        assert app.id is not None
        assert app.company == "TechCorp"
        assert app.status == ApplicationStatus.APPLIED
        
        db.close()

    def test_update_application_status(self):
        """Test updating application status"""
        from datetime import datetime
        db = SessionLocal()
        
        app = Application(
            company="StartupXYZ",
            position="Senior Data Scientist",
            status=ApplicationStatus.APPLIED,
            posted_date=datetime.now(),
        )
        
        db.add(app)
        db.commit()
        db.refresh(app)
        
        # Update status
        app.status = ApplicationStatus.INTERVIEW
        db.commit()
        db.refresh(app)
        
        assert app.status == ApplicationStatus.INTERVIEW
        
        db.close()


class TestInterview:
    def test_create_interview(self):
        """Test creating an interview"""
        from datetime import datetime, timedelta
        db = SessionLocal()
        
        interview = Interview(
            application_id=1,
            company="TechCorp",
            position="ML Engineer",
            type="technical",
            scheduled_at=datetime.now() + timedelta(days=3),
            duration_minutes=60,
            status="scheduled",
        )
        
        db.add(interview)
        db.commit()
        db.refresh(interview)
        
        assert interview.id is not None
        assert interview.type == "technical"
        
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
