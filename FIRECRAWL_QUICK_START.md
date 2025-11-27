# 🚀 Firecrawl Quick Reference

## Setup (5 minutes)

```powershell
# 1. Get API key from https://www.firecrawl.dev/

# 2. Set up environment
cd backend
cp .env.example .env
# Edit .env and add: FIRECRAWL_API_KEY=your_key

# 3. Install packages
pip install -r requirements.txt

# 4. Run server
python app.py
```

## Using the Scraper

**Go to:** `http://localhost:5000/firecrawl-scraper.html`

### Quick Tasks

| Task | Steps |
|------|-------|
| **Scrape 1 job page** | Paste URL → Check auto-import → Click Scrape |
| **Crawl 10 job pages** | Paste site URL → Set limit to 10 → Click Crawl |
| **Import to database** | Check "Auto-import" → Submit |

## API Examples (cURL)

### Scrape a page
```bash
curl -X POST http://localhost:5000/api/scrape-job \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/job/123",
    "auto_add": true,
    "employer_id": 1
  }'
```

### Start crawling
```bash
curl -X POST http://localhost:5000/api/crawl-site \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://jobs.example.com",
    "limit": 5
  }'
```

### Check status
```bash
curl http://localhost:5000/api/crawl-status/crawl_12345?auto_add=true
```

## File Structure

```
PathAI1v4/
├── backend/
│   ├── app.py                    # Main Flask app (updated with endpoints)
│   ├── firecrawl_utils.py        # Scraping logic (NEW)
│   ├── requirements.txt          # Updated with firecrawl-py
│   └── .env.example              # Configuration template (NEW)
├── firecrawl-scraper.html        # Web interface (NEW)
└── FIRECRAWL_INTEGRATION.md      # Full documentation (NEW)
```

## Extracted Data

Each job gets:
- ✅ Title
- ✅ Description (500 char max)
- ✅ Location
- ✅ Remote type (fully_remote/hybrid/on_site)
- ✅ Salary range (if found)
- ✅ Source URL

## Common Issues

| Problem | Solution |
|---------|----------|
| "API key not set" | Create `.env` file in backend folder with key |
| "Website not scraped" | Check if site is public + accessible |
| "Crawl taking too long" | Reduce limit value (try 3-5 instead of 10) |
| "Jobs not importing" | Verify employer_id exists in database |

## Performance

- ⚡ Single page: ~3-5 seconds
- 🕷️ Crawl 5 pages: ~15-30 seconds
- 💾 Auto-import: instant

## Next Steps

1. ✅ Test scraper at `http://localhost:5000/firecrawl-scraper.html`
2. ✅ Try scraping a job site
3. ✅ Auto-import jobs to database
4. ✅ View jobs in Job Search page

---

**Questions?** See `FIRECRAWL_INTEGRATION.md` for full documentation
