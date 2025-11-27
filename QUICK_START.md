# Quick Start Guide - PathAI Website

## 🚀 Fastest Way to Run

### Option 1: Double-Click (Windows)
1. **Double-click `run.bat`** in the project root
2. Wait for the server to start
3. Open `http://localhost:5000` in your browser

### Option 2: PowerShell
1. **Right-click `run.ps1`** → "Run with PowerShell"
2. If you get an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try again.
3. Open `http://localhost:5000` in your browser

## 📋 What You'll See

- **Landing Page** (`http://localhost:5000/`) - Homepage
- **Job Search** - Browse and search jobs
- **Post a Job** - Create job postings (for employers)
- **Application Status** - Track your applications (for candidates)
- **Candidate Inbox** - Review candidates (for employers)
- **Pipeline** - Manage hiring pipeline stages
- **Profile Builder** - Build your candidate profile
- **Resume Parsing** - Upload resumes
- **Skill Gap Analysis** - Analyze skills needed
- **Learning Paths** - Find courses to learn

## ✅ First Steps

1. **Start the server** using one of the methods above
2. **Visit the landing page** at `http://localhost:5000`
3. **Try posting a job:**
   - Click "Post a job" in navigation
   - Fill out the form
   - Submit
4. **Search for jobs:**
   - Go to "Job Search"
   - Use filters or search
   - Click "Apply Now" on any job

## 🔧 Troubleshooting

### "Python not found"
- Install Python 3.8+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Port 5000 already in use"
- Close other applications using port 5000
- Or edit `backend/app.py` line 87 and change `port=5000` to `port=5001`

### "Module not found" errors
- Make sure you're in the `backend` folder when running commands
- Run `pip install -r requirements.txt` again

### Pages not loading
- Make sure the Flask server is running
- Check the terminal for error messages
- Try refreshing the page (Ctrl+F5)

## 📝 Notes

- The database is created automatically on first run
- Sample data can be added through the web interface
- All data is stored in `backend/app.db` (SQLite)
- The server runs in debug mode (auto-reloads on code changes)

## 🎯 Next Steps

1. **Post some jobs** to test the job posting feature
2. **Create applications** by applying to jobs
3. **View applications** in the Application Status page
4. **Explore other features** like skill gap analysis and learning paths

Enjoy using PathAI! 🚀

