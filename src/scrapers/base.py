"""
Base scraper class for job platforms
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import time
import random
from pathlib import Path


@dataclass
class JobScraperConfig:
    """Configuration for job scrapers"""
    base_delay: float = 2.0  # Base delay between requests
    max_delay: float = 5.0   # Maximum delay
    retry_attempts: int = 3
    timeout: int = 30
    headless: bool = True
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    enable_cache: bool = True
    cache_dir: str = "./cache"
    
    def __post_init__(self):
        if self.enable_cache:
            Path(self.cache_dir).mkdir(parents=True, exist_ok=True)


@dataclass
class JobListing:
    """Job listing data structure"""
    platform: str
    job_id: str
    title: str
    company: str
    location: str
    remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "USD"
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    job_url: Optional[str] = None
    posted_date: Optional[datetime] = None
    source_url: Optional[str] = None
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            "platform": self.platform,
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "remote": self.remote,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "currency": self.currency,
            "description": self.description,
            "requirements": self.requirements,
            "skills": ",".join(self.skills),
            "job_url": self.job_url,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "source_url": self.source_url,
            "extracted_at": self.extracted_at.isoformat(),
        }


class JobScraper(ABC):
    """Abstract base class for job scrapers"""
    
    def __init__(self, config: Optional[JobScraperConfig] = None):
        self.config = config or JobScraperConfig()
        self.session = None
        self.headers = {
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    @abstractmethod
    def search(self, keywords: str, location: str = "", company: str = "", remote_only: bool = False) -> List[JobListing]:
        """Search for jobs based on criteria"""
        pass
    
    @abstractmethod
    def parse_job(self, url: str) -> Optional[JobListing]:
        """Parse a single job listing from URL"""
        pass
    
    @abstractmethod
    def login(self, email: str, password: str) -> bool:
        """Authenticate with the platform"""
        pass
    
    def _sleep(self, min_seconds: float = None, max_seconds: float = None):
        """Random sleep with jitter"""
        min_s = min_seconds or self.config.base_delay
        max_s = max_seconds or self.config.max_delay
        delay = random.uniform(min_s, max_s)
        time.sleep(delay)
    
    def _retry_request(self, func, *args, **kwargs) -> Optional[Any]:
        """Retry request with exponential backoff"""
        last_error = None
        
        for attempt in range(self.config.retry_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                self._sleep(min_seconds=2 ** attempt, max_seconds=2 ** (attempt + 1))
        
        raise last_error
    
    def validate_job(self, job: JobListing) -> bool:
        """Validate job listing has required fields"""
        if not job.title or not job.company:
            return False
        if not job.job_id or not job.platform:
            return False
        return True
