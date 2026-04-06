#!/usr/bin/env python3
"""
Run script for Job Application Automation
Run with: python scripts/run.py [api|test|all]
"""
import subprocess
import sys
from pathlib import Path

def run_api():
    """Start the API server"""
    print("🚀 Starting API server on http://localhost:8000")
    print("📖 API docs at http://localhost:8000/docs")
    
    subprocess.run(
        ["python", "-m", "src.api"],
        cwd=Path(__file__).parent.parent
    )

def run_tests():
    """Run all tests"""
    subprocess.run(
        ["python", "scripts/test.py"],
        cwd=Path(__file__).parent.parent
    )

def run_all():
    """Run tests then start API"""
    run_tests()
    run_api()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if mode == "api":
        run_api()
    elif mode == "test":
        run_tests()
    elif mode == "all":
        run_all()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python scripts/run.py [api|test|all]")
        sys.exit(1)
