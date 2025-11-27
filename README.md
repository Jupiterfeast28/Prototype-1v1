Flask backend for the PathAI prototype

Steps to run locally (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Initialize the database

```powershell
python init_db.py
```

4. Run the app

```powershell
python app.py
```

- The server serves the existing `.html` files from the workspace root. Open http://localhost:5000/ to view the site (defaults to `Landing page.html`).
- Simple REST endpoints are available under `/api/*` for `users`, `candidates`, `jobs`, `skills`, and `resumes`.

Notes:
- The original `backend.sql` had Postgres-specific constructs; this backend provides an SQLite-compatible model mapping for key tables.
- If you want a Postgres DB, set `DATABASE_URL` environment variable to a valid SQLAlchemy URL.
