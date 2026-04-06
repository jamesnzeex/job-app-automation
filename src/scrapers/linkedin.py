"""
LinkedIn job scraper
"""
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup
import re
from datetime import datetime

from .base import JobScraper, JobScraperConfig, JobListing


class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn jobs"""
    
    BASE_URL = "https://www.linkedin.com/jobs"
    
    def __init__(self, config: Optional[JobScraperConfig] = None):
        super().__init__(config)
        self.session = None
        self.logged_in = False
    
    def login(self, email: str, password: str) -> bool:
        """Login to LinkedIn - requires browser automation"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.config.headless)
                page = browser.new_page()
                
                # Go to LinkedIn login
                page.goto("https://www.linkedin.com/login")
                
                # Fill credentials
                page.fill("username", email)
                page.fill("password", password)
                page.click('button[type="submit"]')
                
                # Check if login successful
                page.wait_for_load_state("networkidle")
                self.logged_in = "li-login" not in page.content()
                
                browser.close()
                return self.logged_in
                
        except Exception as e:
            print(f"LinkedIn login failed: {e}")
            return False
    
    def search(self, keywords: str, location: str = "", company: str = "", remote_only: bool = False) -> List[JobListing]:
        """Search LinkedIn jobs"""
        from playwright.sync_api import sync_playwright
        
        jobs = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.config.headless)
                page = browser.new_page()
                
                # Build search URL
                search_url = self._build_search_url(keywords, location, company, remote_only)
                
                page.goto(search_url)
                page.wait_for_load_state("networkidle")
                self._sleep(3, 5)  # Wait for JS to load
                
                # Extract jobs
                jobs = self._extract_jobs_from_page(page)
                
                browser.close()
                
        except Exception as e:
            print(f"LinkedIn search failed: {e}")
        
        return jobs
    
    def parse_job(self, url: str) -> Optional[JobListing]:
        """Parse a LinkedIn job page"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.config.headless)
                page = browser.new_page()
                
                page.goto(url)
                page.wait_for_load_state("networkidle")
                self._sleep(2, 3)
                
                content = page.content()
                job = self._parse_job_content(content)
                
                browser.close()
                return job
                
        except Exception as e:
            print(f"Failed to parse LinkedIn job: {e}")
            return None
    
    def _build_search_url(self, keywords: str, location: str = "", company: str = "", remote_only: bool = False) -> str:
        """Build LinkedIn job search URL"""
        url_parts = [
            "https://www.linkedin.com/jobs/search",
            f"keywords={keywords}",
        ]
        
        if location:
            url_parts.append(f"location={location}")
        if company:
            url_parts.append(f"company={company}")
        if remote_only:
            url_parts.append("f_TPR=r8641")  # Remote only filter
        
        return "&".join(url_parts)
    
    def _extract_jobs_from_page(self, page) -> List[JobListing]:
        """Extract jobs from LinkedIn search page"""
        jobs = []
        
        # Find job cards
        job_cards = page.locator("div.job-card-list__title").all()
        
        for card in job_cards[:50]:  # Limit to 50 jobs
            try:
                title = card.locator("h3").inner_text()
                company = card.locator("div.job-card-list__company-name").inner_text()
                location_elem = card.locator("div.job-card-list__location")
                location = location_elem.inner_text() if location_elem.count() > 0 else ""
                
                # Extract URL
                job_link = card.locator("a").get_attribute("href")
                
                # Get job ID from URL
                job_id = self._extract_job_id(job_link)
                
                job = JobListing(
                    platform="linkedin",
                    job_id=job_id,
                    title=title,
                    company=company,
                    location=location,
                    remote="remote" in location.lower(),
                    job_url=f"https://www.linkedin.com{job_link}" if job_link.startswith("/") else job_link,
                    source_url=self._build_search_url(title),
                )
                
                jobs.append(job)
                
            except Exception as e:
                continue
        
        return jobs
    
    def _parse_job_content(self, content: str) -> Optional[JobListing]:
        """Parse job details from page content"""
        soup = BeautifulSoup(content, "html.parser")
        
        try:
            title_elem = soup.find("h1", class_="top-card-layout__title")
            company_elem = soup.find("a", class_="top-card-layout__secondary-entity")
            
            title = title_elem.get_text(strip=True) if title_elem else ""
            company = company_elem.get_text(strip=True) if company_elem else ""
            
            return JobListing(
                platform="linkedin",
                job_id="",
                title=title,
                company=company,
                location="",
                remote=False,
                description=soup.get_text()[:5000],
            )
            
        except Exception:
            return None
    
    def _extract_job_id(self, url: str) -> str:
        """Extract job ID from LinkedIn URL"""
        if not url:
            return ""
        
        # LinkedIn URL formats:
        # /jobs/view/1234567890/
        # https://www.linkedin.com/jobs/view/1234567890
        
        match = re.search(r'/jobs/view/(\d+)', url)
        if match:
            return match.group(1)
        
        return url.split("/")[-1] if url else ""
