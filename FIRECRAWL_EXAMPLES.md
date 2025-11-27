# Firecrawl Integration - Example Workflows

## Example 1: Scrape LinkedIn Job Listings

### Scenario
You want to scrape jobs from LinkedIn's job board

### Steps

```bash
# 1. Find a LinkedIn job listing URL
# Example: https://www.linkedin.com/jobs/view/1234567890/?alternateUrl=...

# 2. API Call
curl -X POST http://localhost:5000/api/scrape-job \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.linkedin.com/jobs/view/1234567890",
    "employer_id": 5,
    "auto_add": true
  }'

# 3. Response
{
  "success": true,
  "job_count": 1,
  "jobs": [
    {
      "title": "Senior Software Engineer",
      "description": "We are looking for a Senior Software Engineer...",
      "location": "San Francisco, CA",
      "remote_type": "hybrid",
      "salary_range": "$180,000 - $250,000",
      "source_url": "https://www.linkedin.com/jobs/view/1234567890",
      "scraped_at": "2024-01-15T10:30:00"
    }
  ]
}

# 4. Job automatically imported to database
# ✅ View in "Job Search" page
```

## Example 2: Crawl Indeed.com for Tech Jobs

### Scenario
You want to collect multiple tech jobs from Indeed

### Steps

```bash
# 1. Start crawl
curl -X POST http://localhost:5000/api/crawl-site \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco",
    "limit": 10,
    "employer_id": 3,
    "auto_add": true
  }'

# 2. Response with Job ID
{
  "success": true,
  "status": "crawling",
  "jobId": "crawl_abc123xyz789",
  "url": "https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco",
  "message": "Crawl started. Use jobId to check status."
}

# 3. Check status (repeat every 5 seconds)
curl http://localhost:5000/api/crawl-status/crawl_abc123xyz789?auto_add=true

# 4. Response while crawling
{
  "success": true,
  "status": "processing",
  "progress": "Crawled 3/10 pages"
}

# 5. Response when complete
{
  "success": true,
  "status": "completed",
  "jobs_added": 32,
  "pages_crawled": 10,
  "message": "Successfully imported 32 jobs"
}

# 6. All jobs now in database
# ✅ View all 32 jobs in "Job Search" with filters
```

## Example 3: Custom Job Board Integration

### Scenario
You have a custom job board and want to scrape it

### URL Pattern
```
https://customjobboard.com/jobs
https://customjobboard.com/jobs?page=1
https://customjobboard.com/jobs?page=2
...
```

### Implementation

```bash
# Option A: Scrape single page
curl -X POST http://localhost:5000/api/scrape-job \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://customjobboard.com/jobs?page=1",
    "employer_id": 1,
    "auto_add": true
  }'

# Option B: Crawl entire job board
curl -X POST http://localhost:5000/api/crawl-site \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://customjobboard.com/jobs",
    "limit": 20,
    "employer_id": 1,
    "auto_add": true
  }'

# Option C: Batch scrape (loop through pages)
for page in {1..10}; do
  curl -X POST http://localhost:5000/api/scrape-job \
    -H "Content-Type: application/json" \
    -d "{
      \"url\": \"https://customjobboard.com/jobs?page=$page\",
      \"employer_id\": 1,
      \"auto_add\": true
    }"
done
```

## Example 4: Scheduled Daily Job Updates (Python Script)

### Scenario
You want to automatically scrape jobs daily

### Python Script
```python
# scrape_jobs_daily.py
import requests
import schedule
import time
from datetime import datetime

API_BASE = "http://localhost:5000/api"

# Job sites to scrape
JOB_SITES = [
    {
        "name": "LinkedIn Tech",
        "url": "https://www.linkedin.com/jobs/search/?keywords=software%20engineer",
        "employer_id": 1,
        "limit": 5
    },
    {
        "name": "Indeed",
        "url": "https://www.indeed.com/jobs?q=python+developer",
        "employer_id": 2,
        "limit": 10
    },
    {
        "name": "GitHub Jobs",
        "url": "https://jobs.github.com/positions?description=ruby",
        "employer_id": 3,
        "limit": 5
    }
]

def scrape_all_sites():
    """Scrape all job sites"""
    print(f"[{datetime.now()}] Starting job scraping...")
    
    total_jobs = 0
    for site in JOB_SITES:
        try:
            response = requests.post(
                f"{API_BASE}/crawl-site",
                json={
                    "url": site["url"],
                    "limit": site["limit"],
                    "employer_id": site["employer_id"],
                    "auto_add": True
                },
                timeout=60
            )
            
            result = response.json()
            if result.get("success"):
                jobs_added = result.get("jobs_added", 0)
                total_jobs += jobs_added
                print(f"✅ {site['name']}: {jobs_added} jobs added")
            else:
                print(f"❌ {site['name']}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ {site['name']}: {str(e)}")
    
    print(f"✅ Scraping complete! Total jobs added: {total_jobs}")

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(scrape_all_sites)

# Keep scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Usage
```powershell
# Run the scheduler
python scrape_jobs_daily.py

# Or schedule with Windows Task Scheduler
# Create task: Run "python C:\path\to\scrape_jobs_daily.py" daily at 2 AM
```

## Example 5: Integrate with Landing Page

### Update Navigation
Edit `Landing page.html`:

```html
<nav>
  <a href="/Job search.html">Job Search</a>
  <a href="/post a job.html">Post a Job</a>
  <a href="/firecrawl-scraper.html">Scrape Jobs</a>  <!-- NEW -->
  <a href="/Candidate inbox.html">Inbox</a>
</nav>
```

### Add to Job Search
Employers can now:
1. Post manual jobs via "Post a Job"
2. Import jobs via "Scrape Jobs" (Firecrawl)
3. View all jobs in "Job Search"

## Example 6: REST API Integration

### Node.js Client
```javascript
// scraper-client.js
const axios = require('axios');

class FirecrawlScraper {
  constructor(baseUrl = 'http://localhost:5000') {
    this.baseUrl = baseUrl;
  }

  async scrapePage(url, employerId = 1, autoAdd = false) {
    try {
      const response = await axios.post(`${this.baseUrl}/api/scrape-job`, {
        url,
        employer_id: employerId,
        auto_add: autoAdd
      });
      return response.data;
    } catch (error) {
      console.error('Scrape failed:', error.message);
      throw error;
    }
  }

  async crawlSite(url, limit = 5, employerId = 1, autoAdd = false) {
    try {
      const response = await axios.post(`${this.baseUrl}/api/crawl-site`, {
        url,
        limit,
        employer_id: employerId,
        auto_add: autoAdd
      });
      return response.data;
    } catch (error) {
      console.error('Crawl failed:', error.message);
      throw error;
    }
  }

  async getCrawlStatus(jobId) {
    try {
      const response = await axios.get(`${this.baseUrl}/api/crawl-status/${jobId}`);
      return response.data;
    } catch (error) {
      console.error('Status check failed:', error.message);
      throw error;
    }
  }
}

// Usage
const scraper = new FirecrawlScraper();
const result = await scraper.scrapePage('https://example.com/job/123', 1, true);
console.log(result);
```

## Example 7: Batch Import with Error Handling

### Python Implementation
```python
# batch_import.py
import requests
import json
from typing import List, Dict

class BatchJobImporter:
    def __init__(self, api_base: str = "http://localhost:5000/api"):
        self.api_base = api_base
        self.imported = []
        self.failed = []
    
    def import_from_urls(self, urls: List[str], employer_id: int = 1):
        """Import jobs from multiple URLs"""
        for url in urls:
            try:
                response = requests.post(
                    f"{self.api_base}/scrape-job",
                    json={
                        "url": url,
                        "employer_id": employer_id,
                        "auto_add": True
                    },
                    timeout=30
                )
                
                result = response.json()
                if result.get("success"):
                    self.imported.append({
                        "url": url,
                        "jobs_found": result.get("job_count", 0)
                    })
                else:
                    self.failed.append({
                        "url": url,
                        "error": result.get("error", "Unknown error")
                    })
                    
            except Exception as e:
                self.failed.append({
                    "url": url,
                    "error": str(e)
                })
        
        self.print_summary()
    
    def print_summary(self):
        """Print import summary"""
        print("\n" + "="*50)
        print(f"✅ Successful: {len(self.imported)}")
        for item in self.imported:
            print(f"   - {item['url']}: {item['jobs_found']} jobs")
        
        if self.failed:
            print(f"\n❌ Failed: {len(self.failed)}")
            for item in self.failed:
                print(f"   - {item['url']}: {item['error']}")
        print("="*50)

# Usage
urls = [
    "https://example.com/job/1",
    "https://example.com/job/2",
    "https://example.com/job/3",
]

importer = BatchJobImporter()
importer.import_from_urls(urls, employer_id=5)
```

## Real-World Scenarios

### Scenario A: Job Portal Launch
```
1. Day 1: Scrape 100 jobs from 5 different job boards
2. Day 1-7: Run daily scrapes to keep listings fresh
3. Week 2: Integrate with email notifications
4. Month 1: Optimize scraper based on user feedback
```

### Scenario B: Talent Acquisition
```
1. HR posts role details in PathAI
2. System scrapes similar jobs from competitors
3. Identifies top candidates from similar roles
4. Automated outreach to passive candidates
```

### Scenario C: Market Research
```
1. Track job market trends over time
2. Analyze salary ranges by location/role
3. Identify skill demand patterns
4. Generate monthly market reports
```

---

**Need help? Check FIRECRAWL_INTEGRATION.md for full documentation**
