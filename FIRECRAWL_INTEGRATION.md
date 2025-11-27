# Firecrawl Integration Guide - PathAI

## 📋 Overview

Firecrawl has been integrated into PathAI to enable automatic web scraping and job data extraction. This allows you to:

- 🔗 **Scrape single job pages** and extract structured job information
- 🕷️ **Crawl entire job sites** to discover and import multiple job listings
- 📊 **Automatically parse** job titles, descriptions, locations, salaries, and remote types
- 💾 **Auto-import jobs** directly into your PathAI database

## 🚀 Getting Started

### 1. Get Firecrawl API Key

1. Visit [Firecrawl](https://www.firecrawl.dev/)
2. Sign up for a free account
3. Copy your API key from the dashboard

### 2. Configure Environment

1. Navigate to the `backend` folder
2. Create a `.env` file from the template:
   ```powershell
   cp .env.example .env
   ```
3. Edit `.env` and add your Firecrawl API key:
   ```
   FIRECRAWL_API_KEY=your_api_key_here
   ```

### 3. Install Dependencies

The Firecrawl package has been added to `requirements.txt`. Install it:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Start the Server

```powershell
python app.py
```

The server will be running at `http://localhost:5000`

### 5. Access Scraper Interface

Open your browser and navigate to:
```
http://localhost:5000/firecrawl-scraper.html
```

## 🔧 How to Use

### Scrape a Single Job Page

1. Enter a job listing URL (e.g., `https://example.com/job/12345`)
2. Optionally specify an Employer ID for database import
3. Check "Auto-import jobs to database" to save directly
4. Click "🔍 Scrape Page"
5. View extracted job information

**Example:**
- URL: `https://linkedin.com/jobs/view/1234567890`
- The system will extract: title, description, location, remote type

### Crawl an Entire Job Site

1. Enter the base URL of a job site (e.g., `https://jobs.example.com`)
2. Set maximum pages to crawl (default: 5)
3. Optionally specify an Employer ID
4. Check "Auto-import jobs to database" if desired
5. Click "🕷️ Start Crawl"
6. Monitor progress - results will update as pages are crawled

**Note:** Crawling is asynchronous. The system will poll for results every 5 seconds.

## 📡 API Endpoints

### 1. Scrape Single Page
```
POST /api/scrape-job
Content-Type: application/json

{
    "url": "https://example.com/job-listing",
    "auto_add": false,
    "employer_id": 1
}

Response:
{
    "success": true,
    "url": "https://example.com/job-listing",
    "jobs": [
        {
            "title": "Senior Developer",
            "description": "...",
            "location": "San Francisco, CA",
            "remote_type": "hybrid",
            "salary_range": "$150,000 - $200,000",
            "source_url": "https://example.com/job-listing",
            "scraped_at": "2024-01-15T10:30:00"
        }
    ],
    "job_count": 1,
    "page_title": "Job Listing | Example Company",
    "scraped_at": "2024-01-15T10:30:00"
}
```

### 2. Start Crawling a Site
```
POST /api/crawl-site
Content-Type: application/json

{
    "url": "https://jobs.example.com",
    "limit": 10,
    "auto_add": false,
    "employer_id": 1
}

Response:
{
    "success": true,
    "status": "crawling",
    "jobId": "crawl_12345abcde",
    "url": "https://jobs.example.com",
    "message": "Crawl started. Use jobId to check status."
}
```

### 3. Check Crawl Status
```
GET /api/crawl-status/{jobId}?auto_add=true&employer_id=1

Response:
{
    "success": true,
    "status": "completed",
    "data": [
        {
            "url": "https://jobs.example.com/page1",
            "markdown": "...",
            "jobs": [...]
        },
        ...
    ],
    "jobs_added": 15
}
```

### 4. Scrape and Auto-Import
```
POST /api/scrape-and-import
Content-Type: application/json

{
    "url": "https://example.com/job-listing",
    "employer_id": 1
}

Response:
{
    "success": true,
    "message": "Successfully imported 1 jobs",
    "jobs": [
        {
            "id": 42,
            "title": "Senior Developer",
            "description": "...",
            "location": "San Francisco, CA",
            ...
        }
    ],
    "imported_at": "2024-01-15T10:30:00"
}
```

## 📊 Job Parsing

The system automatically extracts:

- **Title**: Job position name
- **Description**: Full job description (truncated to 500 chars)
- **Location**: City/region or "Remote"
- **Remote Type**: `fully_remote`, `hybrid`, or `on_site`
- **Salary**: Extracted salary ranges (e.g., "$50,000 - $75,000")
- **Source URL**: Original webpage URL

## 🔍 Understanding the Integration

### Components

1. **`backend/firecrawl_utils.py`** - Core scraping logic
   - `FirecrawlClient`: Handles API communication
   - `JobParser`: Extracts structured data from HTML/Markdown
   - Helper functions for scraping and crawling

2. **`backend/app.py`** - Flask endpoints
   - `/api/scrape-job` - Single page scraping
   - `/api/crawl-site` - Multi-page crawling
   - `/api/crawl-status/{jobId}` - Status checking
   - `/api/scrape-and-import` - Combined scrape + import

3. **`firecrawl-scraper.html`** - Web interface
   - Beautiful UI for job scraping
   - Real-time status updates
   - Job display and import

4. **`backend/.env.example`** - Configuration template

## ⚙️ Configuration

### Environment Variables

- `FIRECRAWL_API_KEY` - Your Firecrawl API key (required)
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)
- `FLASK_ENV` - Flask environment mode (optional)

### Adjusting Scraper Settings

Edit `backend/firecrawl_utils.py` to customize:

```python
# Maximum description length (default: 500)
description = '\n'.join(description_lines).strip()[:500]

# Crawl depth (in firecrawl_utils.py, JobParser class)
'maxDepth': max_depth  # Default: 2
```

## 🎯 Best Practices

1. **Start Small**: Test with 1-2 pages before crawling large sites
2. **Respect Robots.txt**: Only scrape sites that allow it
3. **Use Employer IDs**: Correctly categorize jobs by employer
4. **Monitor API Usage**: Keep track of your Firecrawl API credits
5. **Error Handling**: The system handles network errors gracefully

## 🐛 Troubleshooting

### "FIRECRAWL_API_KEY not set"
- Create `.env` file in the `backend` folder
- Add your API key: `FIRECRAWL_API_KEY=your_key_here`
- Restart the Flask server

### "Crawl failed after multiple attempts"
- Check if the website allows scraping in `robots.txt`
- Verify the URL is correct and accessible
- Try a shorter `limit` value (fewer pages)

### Jobs not appearing in results
- Some websites use JavaScript rendering - Firecrawl handles this automatically
- Check browser console for any JavaScript errors
- Verify the job site structure is standard

### Database import errors
- Ensure the `employer_id` exists in your database
- Check database logs in `backend/app.db`
- Verify all required fields are present

## 📈 Performance Tips

1. **Batch Operations**: Group multiple scrapes into one crawl job
2. **Crawl Depth**: Lower `maxDepth` for faster crawling
3. **Polling Interval**: Adjust polling frequency in the frontend
4. **Pagination**: For large sites, manually specify paginated URLs

## 🔐 Security Notes

- Never commit `.env` file to git - it's in `.gitignore`
- Keep your API key confidential
- The system validates all URLs before scraping
- Database access is managed through Flask routes

## 💡 Example Workflows

### Workflow 1: Import LinkedIn Jobs
```
1. Get a LinkedIn job search URL with filters
2. Go to firecrawl-scraper.html
3. Paste URL in "Scrape Single Job Page"
4. Enable "Auto-import jobs"
5. Click "Scrape Page"
6. Jobs imported to database automatically
```

### Workflow 2: Aggregate From Multiple Sites
```
1. Identify job board URLs
2. For each site, start a crawl with limit=10
3. Monitor status with crawl-status endpoint
4. Once complete, jobs appear in Job Search
```

### Workflow 3: Scheduled Job Updates
```
1. Create a Python script that calls the API endpoints
2. Schedule with Task Scheduler (Windows) or cron (Linux)
3. Automatically refresh job listings daily
```

## 📚 Resources

- [Firecrawl Documentation](https://www.firecrawl.dev/docs)
- [Firecrawl API Reference](https://www.firecrawl.dev/docs/api-reference)
- [PathAI Repository](../)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Firecrawl documentation
3. Check Flask server logs for errors
4. Verify your API key and internet connection

---

**Happy scraping! 🚀**
