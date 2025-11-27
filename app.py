import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sqlalchemy import or_, and_
# Use fixed models file to avoid parsing issues in original models.py
from models_fixed import db, User, Candidate, Employer, Job, Skill, Resume, Application, PipelineStage, PipelineNote
import firecrawl_utils
from firecrawl_utils import scrape_job_page, crawl_job_site, get_crawl_results

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

# Config: use SQLite database file in backend folder by default
db_path = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/debug/demo-mode', methods=['GET'])
def debug_demo_mode():
    """Debug endpoint to check demo mode status"""
    # Force reload environment variables
    import os
    from dotenv import load_dotenv as _load_dotenv
    
    _env_path = os.path.join(os.path.dirname(firecrawl_utils.__file__), '.env')
    _load_dotenv(_env_path, override=True)
    
    # Re-read from environment
    api_key = os.getenv('FIRECRAWL_API_KEY', 'demo_key')
    demo_mode = api_key in ['your_firecrawl_api_key_here', 'demo_key', '']
    
    return jsonify({
        'FIRECRAWL_API_KEY': api_key,
        'DEMO_MODE': demo_mode,
        'DEMO_JOBS_COUNT': len(firecrawl_utils.DEMO_JOBS),
        '_env_path': _env_path,
        'env_file_exists': os.path.exists(_env_path)
    })

@app.route('/api/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])
    data = request.json or {}
    u = User(email=data.get('email'), role=data.get('role','candidate'))
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@app.route('/api/candidates', methods=['GET','POST'])
def candidates():
    if request.method == 'GET':
        cs = Candidate.query.all()
        return jsonify([c.to_dict() for c in cs])
    data = request.json or {}
    c = Candidate(user_id=data.get('user_id'), headline=data.get('headline'), summary=data.get('summary'))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201

@app.route('/api/jobs', methods=['GET','POST'])
def jobs():
    if request.method == 'GET':
        # Support filtering
        query = Job.query.filter_by(is_active=True)
        
        # Filter by location
        location = request.args.get('location')
        if location:
            query = query.filter(Job.location.contains(location))
        
        # Filter by keywords in title or description
        keywords = request.args.get('keywords')
        if keywords:
            query = query.filter(or_(
                Job.title.contains(keywords),
                Job.description.contains(keywords)
            ))
        
        # Filter by salary range
        salary_min = request.args.get('salary_min')
        if salary_min:
            query = query.filter(Job.salary_min >= float(salary_min))
        
        js = query.all()
        return jsonify([j.to_dict() for j in js])
    
    data = request.json or {}
    j = Job(
        employer_id=data.get('employer_id'),
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        remote_type=data.get('remote_type'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max')
    )
    db.session.add(j)
    db.session.commit()
    return jsonify(j.to_dict()), 201

@app.route('/api/skills', methods=['GET','POST'])
def skills():
    if request.method == 'GET':
        s = Skill.query.all()
        return jsonify([x.to_dict() for x in s])
    data = request.json or {}
    sk = Skill(name=data.get('name'))
    db.session.add(sk)
    db.session.commit()
    return jsonify(sk.to_dict()), 201

@app.route('/api/resumes', methods=['GET','POST'])
def resumes():
    if request.method == 'GET':
        r = Resume.query.all()
        return jsonify([x.to_dict() for x in r])
    data = request.json or {}
    r = Resume(candidate_id=data.get('candidate_id'), file_name=data.get('file_name'), file_type=data.get('file_type'))
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201

@app.route('/api/applications', methods=['GET','POST'])
def applications():
    if request.method == 'GET':
        # Support filtering by candidate_id or job_id
        query = Application.query
        candidate_id = request.args.get('candidate_id')
        job_id = request.args.get('job_id')
        if candidate_id:
            query = query.filter_by(candidate_id=candidate_id)
        if job_id:
            query = query.filter_by(job_id=job_id)
        apps = query.all()
        return jsonify([a.to_dict() for a in apps])
    
    data = request.json or {}
    app = Application(
        candidate_id=data.get('candidate_id'),
        job_id=data.get('job_id'),
        current_status=data.get('current_status', 'Applied')
    )
    db.session.add(app)
    db.session.commit()
    return jsonify(app.to_dict()), 201

@app.route('/api/applications/<int:app_id>', methods=['GET','PUT','PATCH'])
def application_detail(app_id):
    app = Application.query.get_or_404(app_id)
    if request.method == 'GET':
        return jsonify(app.to_dict())
    
    data = request.json or {}
    if 'current_status' in data:
        app.current_status = data['current_status']
    db.session.commit()
    return jsonify(app.to_dict())

@app.route('/api/pipeline/stages', methods=['GET','POST'])
def pipeline_stages():
    if request.method == 'GET':
        stages = PipelineStage.query.all()
        return jsonify([{'stage_id': s.stage_id, 'name': s.name} for s in stages])
    
    data = request.json or {}
    stage = PipelineStage(name=data.get('name'))
    db.session.add(stage)
    db.session.commit()
    return jsonify({'stage_id': stage.stage_id, 'name': stage.name}), 201

@app.route('/api/pipeline/notes', methods=['GET','POST'])
def pipeline_notes():
    if request.method == 'GET':
        query = PipelineNote.query
        application_id = request.args.get('application_id')
        if application_id:
            query = query.filter_by(application_id=application_id)
        notes = query.all()
        return jsonify([{
            'note_id': n.note_id,
            'application_id': n.application_id,
            'author_id': n.author_id,
            'note_text': n.note_text,
            'created_at': n.created_at.isoformat() if n.created_at else None
        } for n in notes])
    
    data = request.json or {}
    note = PipelineNote(
        application_id=data.get('application_id'),
        author_id=data.get('author_id'),
        note_text=data.get('note_text')
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({
        'note_id': note.note_id,
        'application_id': note.application_id,
        'author_id': note.author_id,
        'note_text': note.note_text,
        'created_at': note.created_at.isoformat() if note.created_at else None
    }), 201

# ============================================================================
# Firecrawl Integration Endpoints
# ============================================================================

@app.route('/api/scrape-job', methods=['POST'])
def scrape_job():
    """
    Scrape a single job page and extract job information.
    
    Request JSON:
    {
        "url": "https://example.com/job-listing",
        "auto_add": false  // Optional: automatically add jobs to database
    }
    """
    try:
        data = request.json or {}
        url = data.get('url')
        auto_add = data.get('auto_add', False)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Scrape the page
        result = scrape_job_page(url)
        
        # Optionally add jobs to database
        if auto_add and result.get('success') and result.get('jobs'):
            for job_data in result['jobs']:
                job = Job(
                    employer_id=data.get('employer_id', 1),
                    title=job_data.get('title'),
                    description=job_data.get('description'),
                    location=job_data.get('location', 'Remote'),
                    remote_type=job_data.get('remote_type', 'hybrid'),
                    is_active=True
                )
                db.session.add(job)
            db.session.commit()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/crawl-site', methods=['POST'])
def crawl_site():
    """
    Crawl a job site and extract multiple job listings.
    This starts an async crawl job.
    
    Request JSON:
    {
        "url": "https://example.com/jobs",
        "limit": 10,
        "auto_add": false
    }
    """
    try:
        data = request.json or {}
        url = data.get('url')
        limit = data.get('limit', 10)
        auto_add = data.get('auto_add', False)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Start crawl
        result = crawl_job_site(url, limit=limit)
        
        # Store auto_add preference for later retrieval
        if auto_add:
            result['auto_add'] = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/crawl-status/<job_id>', methods=['GET'])
def crawl_status(job_id):
    """
    Check the status and results of an async crawl job.
    
    URL parameter:
        job_id: The crawl job ID from the crawl-site endpoint
    
    Query parameters:
        auto_add: true to automatically add jobs to database when complete
    """
    try:
        auto_add = request.args.get('auto_add', 'false').lower() == 'true'
        
        # Get crawl status
        result = get_crawl_results(job_id)
        
        # If crawl is complete and auto_add is enabled, add jobs to database
        if auto_add and result.get('success') and result.get('status') == 'completed':
            jobs_data = result.get('data', [])
            added_count = 0
            
            for item in jobs_data:
                # Jobs are already extracted in the crawl result
                # Add them to the database
                for job_info in item.get('jobs', []):
                    job = Job(
                        employer_id=request.args.get('employer_id', 1),
                        title=job_info.get('title'),
                        description=job_info.get('description'),
                        location=job_info.get('location', 'Remote'),
                        remote_type=job_info.get('remote_type', 'hybrid'),
                        is_active=True
                    )
                    db.session.add(job)
                    added_count += 1
            
            if added_count > 0:
                db.session.commit()
                result['jobs_added'] = added_count
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scrape-and-import', methods=['POST'])
def scrape_and_import():
    """
    Scrape a job page, parse jobs, and automatically import them.
    
    Request JSON:
    {
        "url": "https://example.com/job-listing",
        "employer_id": 1,
        "job_title": "Optional override for parsed title"
    }
    """
    try:
        data = request.json or {}
        url = data.get('url')
        employer_id = data.get('employer_id', 1)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Scrape the page
        scrape_result = scrape_job_page(url)
        
        if not scrape_result.get('success'):
            return jsonify(scrape_result), 400
        
        # Import jobs to database
        imported_jobs = []
        for job_data in scrape_result.get('jobs', []):
            job = Job(
                employer_id=employer_id,
                title=job_data.get('title'),
                description=job_data.get('description'),
                location=job_data.get('location', 'Remote'),
                remote_type=job_data.get('remote_type', 'hybrid'),
                is_active=True
            )
            db.session.add(job)
            db.session.flush()  # Flush to get the ID
            imported_jobs.append(job.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully imported {len(imported_jobs)} jobs',
            'jobs': imported_jobs,
            'imported_at': result.get('scraped_at')
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Serve existing frontend files from workspace root
@app.route('/', defaults={'path': 'Landing page.html'})
@app.route('/<path:path>')
def static_proxy(path):
    # Serve a file from the workspace root
    root = app.static_folder
    if os.path.exists(os.path.join(root, path)):
        return send_from_directory(root, path)
    return send_from_directory(root, 'Landing page.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
