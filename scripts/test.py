#!/usr/bin/env python3
"""
Test runner script
Run with: python scripts/test.py
"""
import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests"""
    test_dir = Path(__file__).parent.parent / "tests"
    
    print("🧪 Running tests...")
    print("=" * 50)
    
    result = subprocess.run(
        ["pytest", str(test_dir), "-v", "--tb=short"],
        cwd=Path(__file__).parent.parent
    )
    
    print("=" * 50)
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {result.returncode} tests failed")
    
    return result.returncode

def test_api():
    """Test API endpoints"""
    print("🧪 Testing API...")
    
    from src.api.main import app
    from src.models.database import init_db, get_db
    from src.models.models import Application
    
    init_db()
    db = next(get_db())
    
    # Test create application
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    response = client.post("/api/applications", json={
        "company": "TestCorp",
        "position": "ML Engineer",
        "job_url": "https://test.com/job",
        "platform": "linkedin",
        "status": "applied",
        "posted_date": "2026-04-06T20:00:00",
        "location": "Remote",
        "remote": True,
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["company"] == "TestCorp"
    assert data["position"] == "ML Engineer"
    
    print("✅ API tests passed!")
    db.close()

def test_database():
    """Test database operations"""
    print("🧪 Testing database...")
    
    from src.models.database import init_db, SessionLocal
    from src.models.models import Application, ApplicationStatus
    
    init_db()
    db = SessionLocal()
    
    # Create test application
    app = Application(
        company="DatabaseTest",
        position="Data Scientist",
        status=ApplicationStatus.APPLIED,
    )
    
    db.add(app)
    db.commit()
    db.refresh(app)
    
    assert app.id is not None
    print(f"✅ Database test created application with ID: {app.id}")
    
    # Test query
    apps = db.query(Application).all()
    print(f"✅ Found {len(apps)} applications in database")
    
    db.close()

if __name__ == "__main__":
    print("🚀 Job Application Automation - Test Suite")
    print("=" * 50)
    
    test_database()
    test_api()
    
    # Run pytest
    run_tests()
