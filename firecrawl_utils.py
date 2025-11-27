"""
Firecrawl integration utilities for scraping job listings and websites.
Helps automatically populate the job database with data from various job boards.
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Ensure we load the .env located next to this module (backend/.env)
_env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_env_path, override=True)

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY', 'demo_key')
FIRECRAWL_API_URL = 'https://api.firecrawl.dev/v0'

def is_demo_mode() -> bool:
    """Check if demo mode is enabled (called at runtime, not import time)"""
    api_key = os.getenv('FIRECRAWL_API_KEY', 'demo_key')
    return api_key in ['your_firecrawl_api_key_here', 'demo_key', '']

# For backward compatibility at module level
DEMO_MODE = is_demo_mode()


# Demo data for testing
DEMO_JOBS = [
    {
        "title": "Senior Full-Stack Engineer",
        "description": "We're looking for a senior full-stack engineer with 5+ years of experience. You'll work on scalable web applications using React, Python, and AWS.",
        "location": "San Francisco, CA",
        "remote_type": "hybrid",
        "salary_range": "$150,000 - $200,000"
    },
    {
        "title": "DevOps Engineer",
        "description": "Join our infrastructure team to design and maintain cloud systems. Experience with Kubernetes, Docker, and CI/CD pipelines required.",
        "location": "New York, NY",
        "remote_type": "fully_remote",
        "salary_range": "$120,000 - $160,000"
    },
    {
        "title": "Product Manager",
        "description": "Lead product strategy and roadmap for our SaaS platform. You'll work cross-functionally with engineering and design teams.",
        "location": "Remote",
        "remote_type": "fully_remote",
        "salary_range": "$140,000 - $180,000"
    }
]


class FirecrawlClient:
    """Client for interacting with Firecrawl API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Firecrawl client with API key"""
        self.api_key = api_key or FIRECRAWL_API_KEY
        self.demo_mode = is_demo_mode()  # Check at runtime, not import time
        if not self.demo_mode and not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable not set")
        self.base_url = FIRECRAWL_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def scrape_page(self, url: str, markdown: bool = True) -> Dict:
        """
        Scrape a single page using Firecrawl
        
        Args:
            url: The URL to scrape
            markdown: Whether to return content in markdown format
            
        Returns:
            Dictionary with scraped content
        """
        # Demo mode: return mock data
        if self.demo_mode:
            import random
            job = random.choice(DEMO_JOBS)
            return {
                'success': True,
                'markdown': f"# {job['title']}\n\n{job['description']}",
                'pageTitle': job['title'],
                'metadata': {'url': url}
            }
        
        try:
            endpoint = f'{self.base_url}/scrape'
            payload = {
                'url': url,
                'markdown': markdown,
                'waitForSelector': None
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def crawl_site(self, url: str, limit: int = 5, max_depth: int = 2) -> Dict:
        """
        Crawl multiple pages from a website
        
        Args:
            url: The starting URL to crawl
            limit: Maximum number of pages to crawl
            max_depth: Maximum depth of crawling
            
        Returns:
            Dictionary with crawl results
        """
        # Demo mode: return mock data
        if self.demo_mode:
            return {
                'success': True,
                'jobId': f'demo_crawl_{int(datetime.now().timestamp())}',
                'status': 'completed',
                'data': [
                    {'url': f'{url}?page={i+1}', 'markdown': f"# Job {i+1}\n\n{job['description']}", 'jobs': [job]}
                    for i, job in enumerate(DEMO_JOBS[:limit])
                ]
            }
        
        try:
            endpoint = f'{self.base_url}/crawl'
            payload = {
                'url': url,
                'limit': limit,
                'maxDepth': max_depth,
                'markdown': True,
                'waitForSelector': None
            }
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # For async crawling, return the job ID
            if 'jobId' in result:
                return {
                    'success': True,
                    'jobId': result['jobId'],
                    'status': 'processing'
                }
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def get_crawl_status(self, job_id: str) -> Dict:
        """Get status of a crawl job"""
        try:
            endpoint = f'{self.base_url}/crawl/{job_id}'
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'jobId': job_id
            }


class JobParser:
    """Parse and extract job information from scraped content"""
    
    @staticmethod
    def extract_jobs_from_page(content: str, url: str) -> List[Dict]:
        """
        Extract job listings from scraped page content
        Uses pattern matching to identify job-like entries
        
        Args:
            content: The scraped page content (markdown or HTML)
            url: The source URL
            
        Returns:
            List of extracted job dictionaries
        """
        jobs = []
        
        # Split by common job separators
        job_sections = re.split(r'\n#{1,3}\s+|\n-{3,}|\n\*{3,}', content)
        
        for section in job_sections:
            if len(section.strip()) > 50:  # Minimum content length
                job = JobParser._parse_job_section(section, url)
                if job:
                    jobs.append(job)
        
        return jobs
    
    @staticmethod
    def _parse_job_section(section: str, source_url: str) -> Optional[Dict]:
        """Parse a single job section"""
        lines = section.strip().split('\n')
        
        # Try to extract title (first line or line with job title keywords)
        title = None
        description_lines = []
        location = None
        salary_range = None
        remote_type = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Extract title
            if not title and (
                'job title' in line_lower or 
                'position' in line_lower or 
                'role:' in line_lower or
                (i == 0 and len(line) > 5 and len(line) < 200)
            ):
                title = line.replace('Job Title:', '').replace('Position:', '').replace('Role:', '').strip()
            
            # Extract location
            if 'location' in line_lower or 'city' in line_lower:
                location = re.sub(r'(location|city|where)[:*\-]*', '', line, flags=re.IGNORECASE).strip()
            
            # Extract remote type
            if 'remote' in line_lower or 'work' in line_lower:
                if 'fully remote' in line_lower or 'work from anywhere' in line_lower:
                    remote_type = 'fully_remote'
                elif 'hybrid' in line_lower:
                    remote_type = 'hybrid'
                elif 'on-site' in line_lower or 'office' in line_lower:
                    remote_type = 'on_site'
            
            # Extract salary
            salary_pattern = r'\$[\d,]+\s*-\s*\$[\d,]+'
            salary_match = re.search(salary_pattern, line)
            if salary_match:
                salary_range = salary_match.group(0)
            
            # Collect description lines
            if not any(keyword in line_lower for keyword in ['location', 'salary', 'remote', 'job title', 'position', 'role']):
                description_lines.append(line)
        
        description = '\n'.join(description_lines).strip()[:500]
        
        # Only return if we have meaningful content
        if title and (description or location):
            return {
                'title': title[:100],
                'description': description,
                'location': location or 'Remote',
                'remote_type': remote_type or 'hybrid',
                'salary_range': salary_range,
                'source_url': source_url,
                'scraped_at': datetime.now().isoformat()
            }
        
        return None


def scrape_job_page(url: str) -> Dict:
    """
    Scrape a single job page and extract job information
    
    Args:
        url: The URL to scrape
        
    Returns:
        Dictionary with scrape results and extracted jobs
    """
    try:
        client = FirecrawlClient()
        result = client.scrape_page(url)
        
        if not result.get('success', False):
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'url': url
            }
        
        # In demo mode, return demo jobs directly
        if is_demo_mode():
            import random
            jobs = [random.choice(DEMO_JOBS)]
        else:
            content = result.get('markdown', result.get('content', ''))
            jobs = JobParser.extract_jobs_from_page(content, url)
        
        return {
            'success': True,
            'url': url,
            'jobs': jobs,
            'job_count': len(jobs),
            'page_title': result.get('pageTitle', 'Unknown'),
            'scraped_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }


def crawl_job_site(url: str, limit: int = 10) -> Dict:
    """
    Crawl a job site and extract multiple job listings
    
    Args:
        url: The job site URL to start crawling from
        limit: Maximum number of pages to crawl
        
    Returns:
        Dictionary with crawl results
    """
    try:
        client = FirecrawlClient()
        result = client.crawl_site(url, limit=limit)
        
        if not result.get('success', False):
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'url': url
            }
        
        # Async job - return job ID for polling
        if 'jobId' in result:
            return {
                'success': True,
                'status': 'crawling',
                'jobId': result['jobId'],
                'url': url,
                'message': 'Crawl started. Use jobId to check status.'
            }
        
        # Process results if available
        jobs = []
        data = result.get('data', [])
        
        for item in data:
            content = item.get('markdown', item.get('content', ''))
            extracted = JobParser.extract_jobs_from_page(content, item.get('url', url))
            jobs.extend(extracted)
        
        return {
            'success': True,
            'url': url,
            'jobs': jobs,
            'job_count': len(jobs),
            'pages_crawled': len(data),
            'crawled_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url
        }


def get_crawl_results(job_id: str) -> Dict:
    """Check the status and results of an async crawl job"""
    try:
        client = FirecrawlClient()
        return client.get_crawl_status(job_id)
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'jobId': job_id
        }
