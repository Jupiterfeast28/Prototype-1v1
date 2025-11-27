# PathAI - Job Matching Platform

A full-stack job matching platform built with Flask backend and HTML/CSS/JavaScript frontend.

## Features

- **Job Search**: Browse and filter jobs by location, salary, and keywords
- **Job Posting**: Employers can post new job listings
- **Application Tracking**: Candidates can track their application status
- **Candidate Inbox**: Employers can review and manage candidate applications
- **Pipeline Management**: Visual pipeline for managing hiring stages
- **Profile Builder**: Candidates can build and edit their profiles
- **Resume Parsing**: Upload and parse resumes
- **Skill Gap Analysis**: Analyze skills needed for job roles
- **Learning Paths**: Discover courses to bridge skill gaps

## Quick Start

### Windows (PowerShell)

1. **Run the setup script:**
   ```powershell
   .\run.ps1
   ```

   Or double-click `run.bat` if you prefer Command Prompt.

2. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - The landing page will load automatically

### Manual Setup

1. **Navigate to backend folder:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```powershell
   python init_db.py
   ```

5. **Run the server:**
   ```powershell
   python app.py
   ```

6. **Open browser:**
   - Go to `http://localhost:5000`

## Project Structure

```
PathAI1v2/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── models_fixed.py     # Database models
│   ├── init_db.py          # Database initialization
│   ├── requirements.txt    # Python dependencies
│   └── app.db             # SQLite database (created on first run)
├── Landing page.html       # Homepage
├── Job search.html         # Job search and browsing
├── post a job.html         # Job posting form
├── Application Status.html # Application tracking
├── Candidate inbox.html    # Employer candidate management
├── pipeline.html           # Hiring pipeline visualization
├── profile builder.html    # Candidate profile builder
├── resume parsing.html      # Resume upload and parsing
├── skill gap analysis.html # Skill analysis tool
├── Learning.html           # Learning paths
├── api.js                  # Frontend API helper
├── run.bat                 # Windows batch script to run
├── run.ps1                 # PowerShell script to run
└── README.md              # This file
```

## API Endpoints

### Jobs
- `GET /api/jobs` - List all active jobs (supports `?keywords=`, `?location=`, `?salary_min=`)
- `POST /api/jobs` - Create a new job posting

### Applications
- `GET /api/applications` - List applications (supports `?candidate_id=`, `?job_id=`)
- `POST /api/applications` - Submit a new application
- `GET /api/applications/<id>` - Get application details
- `PUT /api/applications/<id>` - Update application status

### Pipeline
- `GET /api/pipeline/stages` - List all pipeline stages
- `POST /api/pipeline/stages` - Create a new stage
- `GET /api/pipeline/notes` - List notes (supports `?application_id=`)
- `POST /api/pipeline/notes` - Add a note to an application

### Other
- `GET /api/users` - List users
- `GET /api/candidates` - List candidates
- `GET /api/skills` - List skills
- `GET /api/resumes` - List resumes

## Pages

- **Landing Page** (`/` or `/Landing page.html`) - Homepage with features overview
- **Job Search** (`/Job search.html`) - Browse and search jobs
- **Post a Job** (`/post a job.html`) - Create new job postings
- **Application Status** (`/Application Status.html`) - Track your applications
- **Candidate Inbox** (`/Candidate inbox.html`) - Review candidates (employers)
- **Pipeline** (`/pipeline.html`) - Manage hiring pipeline
- **Profile Builder** (`/profile builder.html`) - Build candidate profile
- **Resume Parsing** (`/resume parsing.html`) - Upload and parse resumes
- **Skill Gap Analysis** (`/skill gap analysis.html`) - Analyze skill gaps
- **Learning Paths** (`/Learning.html`) - Discover learning resources

## Database

The application uses SQLite by default (stored in `backend/app.db`). The database schema is based on the provided `backend.sql` file and includes:

- Users (candidates, employers, admins)
- Jobs and job postings
- Applications and application status
- Candidates and their profiles
- Skills and skill matching
- Resumes and parsed resume data
- Pipeline stages and notes
- Learning paths

## Development

### Adding New Features

1. **Backend**: Add new routes in `backend/app.py`
2. **Frontend**: Create or update HTML pages in the root directory
3. **API Integration**: Use `api.js` helper functions or fetch directly

### Database Changes

1. Update models in `backend/models_fixed.py`
2. Run `python backend/init_db.py` to recreate tables
3. Note: This will reset the database!

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, edit `backend/app.py` and change:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```
to a different port (e.g., `port=5001`).

### Python Not Found
- Make sure Python 3.8+ is installed
- Add Python to your system PATH
- Or use full path: `C:\Python39\python.exe -m venv .venv`

### Database Errors
- Delete `backend/app.db` and run `python backend/init_db.py` again
- Check that all models are properly defined in `models_fixed.py`

## License

This is a prototype/demo project.

## Support

For issues or questions, check the code comments or review the API endpoints in `backend/app.py`.

