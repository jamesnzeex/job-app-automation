"""
Job Scrapers Module

Provides job scraping functionality for LinkedIn and Indeed platforms.
"""

from .base import JobScraper, JobScraperConfig
from .linkedin import LinkedInScraper
from .indeed import IndeedScraper
from .job_matcher import JobMatcher, JobCriteria
from .utils import format_salary, parse_job_url, extract_job_id

__all__ = [
    "JobScraper",
    "JobScraperConfig",
    "LinkedInScraper",
    "IndeedScraper",
    "JobMatcher",
    "JobCriteria",
    "format_salary",
    "parse_job_url",
    "extract_job_id",
]
