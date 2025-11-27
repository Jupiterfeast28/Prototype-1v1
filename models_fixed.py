from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)
    oauth_provider = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate = db.relationship('Candidate', backref='user', uselist=False)
    employer = db.relationship('Employer', backref='user', uselist=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role
        }

class Candidate(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    headline = db.Column(db.String)
    summary = db.Column(db.Text)
    salary_expectation = db.Column(db.Numeric)
    location = db.Column(db.String)
    visibility = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    resumes = db.relationship('Resume', backref='candidate')
    skills = db.relationship('CandidateSkill', backref='candidate')

    def to_dict(self):
        return {
            'candidate_id': self.candidate_id,
            'user_id': self.user_id,
            'headline': self.headline,
            'summary': self.summary,
            'location': self.location
        }

class Employer(db.Model):
    __tablename__ = 'employers'
    employer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    company_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship('Job', backref='employer')

    def to_dict(self):
        return {'employer_id': self.employer_id, 'company_name': self.company_name}

class Skill(db.Model):
    __tablename__ = 'skills'
    skill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {'skill_id': self.skill_id, 'name': self.name}

class CandidateSkill(db.Model):
    __tablename__ = 'candidate_skills'
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.candidate_id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), primary_key=True)
    proficiency = db.Column(db.Integer)

class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.employer_id'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    remote_type = db.Column(db.String)
    salary_min = db.Column(db.Numeric)
    salary_max = db.Column(db.Numeric)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'job_id': self.job_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'is_active': self.is_active
        }

class Resume(db.Model):
    __tablename__ = 'resumes'
    resume_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.candidate_id'))
    file_name = db.Column(db.String)
    file_type = db.Column(db.String)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    parsed_title = db.Column(db.String)
    parsed_summary = db.Column(db.Text)

    def to_dict(self):
        return {'resume_id': self.resume_id, 'candidate_id': self.candidate_id, 'file_name': self.file_name}

class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.candidate_id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    current_status = db.Column(db.String, default='Applied')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'application_id': self.application_id, 'candidate_id': self.candidate_id, 'job_id': self.job_id, 'status': self.current_status}

class PipelineStage(db.Model):
    __tablename__ = 'pipeline_stages'
    stage_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class PipelineNote(db.Model):
    __tablename__ = 'pipeline_notes'
    note_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.application_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    note_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
