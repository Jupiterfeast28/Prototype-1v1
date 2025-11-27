-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.Users (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  name text,
  email text NOT NULL UNIQUE,
  CONSTRAINT Users_pkey PRIMARY KEY (id)
);
CREATE TABLE public.ai_job_readiness_scores (
  score_id integer NOT NULL DEFAULT nextval('ai_job_readiness_scores_score_id_seq'::regclass),
  candidate_id integer,
  job_id integer,
  readiness_score numeric NOT NULL,
  recency_score numeric,
  last_calculated timestamp without time zone DEFAULT now(),
  CONSTRAINT ai_job_readiness_scores_pkey PRIMARY KEY (score_id),
  CONSTRAINT ai_job_readiness_scores_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id),
  CONSTRAINT ai_job_readiness_scores_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id)
);
CREATE TABLE public.ai_skill_match_details (
  detail_id integer NOT NULL DEFAULT nextval('ai_skill_match_details_detail_id_seq'::regclass),
  readiness_score_id integer,
  skill_id integer,
  match_status character varying NOT NULL CHECK (match_status::text = ANY (ARRAY['Matched'::character varying, 'Gap'::character varying, 'Surplus'::character varying]::text[])),
  match_percentage numeric,
  explanation_text text,
  CONSTRAINT ai_skill_match_details_pkey PRIMARY KEY (detail_id),
  CONSTRAINT ai_skill_match_details_readiness_score_id_fkey FOREIGN KEY (readiness_score_id) REFERENCES public.ai_job_readiness_scores(score_id),
  CONSTRAINT ai_skill_match_details_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id)
);
CREATE TABLE public.application_notes (
  id integer NOT NULL DEFAULT nextval('application_notes_id_seq'::regclass),
  application_id integer,
  author_id integer,
  note text NOT NULL,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT application_notes_pkey PRIMARY KEY (id)
);
CREATE TABLE public.application_pipeline (
  application_id integer NOT NULL,
  stage_id integer NOT NULL,
  moved_at timestamp without time zone DEFAULT now(),
  CONSTRAINT application_pipeline_pkey PRIMARY KEY (application_id, stage_id),
  CONSTRAINT application_pipeline_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id),
  CONSTRAINT application_pipeline_stage_id_fkey FOREIGN KEY (stage_id) REFERENCES public.pipeline_stages(stage_id)
);
CREATE TABLE public.applications (
  application_id integer NOT NULL DEFAULT nextval('applications_application_id_seq'::regclass),
  candidate_id integer,
  job_id integer,
  current_status character varying DEFAULT 'Applied'::character varying,
  applied_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT applications_pkey PRIMARY KEY (application_id),
  CONSTRAINT applications_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id),
  CONSTRAINT applications_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id)
);
CREATE TABLE public.audit_logs (
  log_id integer NOT NULL DEFAULT nextval('audit_logs_log_id_seq'::regclass),
  user_id integer,
  action character varying NOT NULL,
  details jsonb,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT audit_logs_pkey PRIMARY KEY (log_id),
  CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.billings (
  id integer NOT NULL DEFAULT nextval('billings_id_seq'::regclass),
  employer_id integer,
  plan USER-DEFINED DEFAULT 'basic'::billing_plan,
  start_date date NOT NULL,
  end_date date,
  amount numeric,
  status USER-DEFINED DEFAULT 'active'::billing_status,
  CONSTRAINT billings_pkey PRIMARY KEY (id)
);
CREATE TABLE public.candidate_profiles (
  user_id integer NOT NULL,
  headline character varying,
  summary text,
  location character varying,
  salary_expectation numeric,
  visibility boolean DEFAULT false,
  skills_vector tsvector,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT candidate_profiles_pkey PRIMARY KEY (user_id)
);
CREATE TABLE public.candidate_skills (
  candidate_id integer NOT NULL,
  skill_id integer NOT NULL,
  proficiency integer CHECK (proficiency >= 1 AND proficiency <= 100),
  CONSTRAINT candidate_skills_pkey PRIMARY KEY (candidate_id, skill_id),
  CONSTRAINT candidate_skills_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id),
  CONSTRAINT candidate_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id)
);
CREATE TABLE public.candidates (
  candidate_id integer NOT NULL DEFAULT nextval('candidates_candidate_id_seq'::regclass),
  user_id integer UNIQUE,
  headline character varying,
  summary text,
  salary_expectation numeric,
  location character varying,
  visibility boolean DEFAULT false,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT candidates_pkey PRIMARY KEY (candidate_id),
  CONSTRAINT candidates_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.educations (
  id integer NOT NULL DEFAULT nextval('educations_id_seq'::regclass),
  user_id integer,
  degree character varying,
  institution character varying,
  field character varying,
  location character varying,
  start_date date,
  end_date date,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT educations_pkey PRIMARY KEY (id)
);
CREATE TABLE public.employers (
  employer_id integer NOT NULL DEFAULT nextval('employers_employer_id_seq'::regclass),
  user_id integer UNIQUE,
  company_name character varying NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT employers_pkey PRIMARY KEY (employer_id),
  CONSTRAINT employers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.job_alerts (
  alert_id integer NOT NULL DEFAULT nextval('job_alerts_alert_id_seq'::regclass),
  candidate_id integer,
  job_tags ARRAY,
  location character varying,
  remote_type character varying CHECK (remote_type IS NULL OR (remote_type::text = ANY (ARRAY['remote'::character varying, 'hybrid'::character varying, 'on-site'::character varying]::text[]))),
  created_at timestamp without time zone DEFAULT now(),
  last_sent timestamp without time zone,
  CONSTRAINT job_alerts_pkey PRIMARY KEY (alert_id),
  CONSTRAINT job_alerts_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id)
);
CREATE TABLE public.job_applications_stats (
  job_id integer NOT NULL,
  total_applications integer DEFAULT 0,
  total_views integer DEFAULT 0,
  CONSTRAINT job_applications_stats_pkey PRIMARY KEY (job_id),
  CONSTRAINT job_applications_stats_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id)
);
CREATE TABLE public.job_required_skills (
  job_id integer NOT NULL,
  skill_id integer NOT NULL,
  required_proficiency integer DEFAULT 50 CHECK (required_proficiency >= 1 AND required_proficiency <= 100),
  CONSTRAINT job_required_skills_pkey PRIMARY KEY (job_id, skill_id),
  CONSTRAINT job_required_skills_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id),
  CONSTRAINT job_required_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id)
);
CREATE TABLE public.job_skills (
  id integer NOT NULL DEFAULT nextval('job_skills_id_seq'::regclass),
  job_id integer,
  skill_id integer,
  required_level USER-DEFINED DEFAULT 'intermediate'::skill_level,
  CONSTRAINT job_skills_pkey PRIMARY KEY (id)
);
CREATE TABLE public.job_tags (
  id integer NOT NULL DEFAULT nextval('job_tags_id_seq'::regclass),
  job_id integer,
  tag character varying NOT NULL,
  CONSTRAINT job_tags_pkey PRIMARY KEY (id)
);
CREATE TABLE public.job_views (
  view_id integer NOT NULL DEFAULT nextval('job_views_view_id_seq'::regclass),
  job_id integer,
  viewer_id integer,
  viewed_at timestamp without time zone DEFAULT now(),
  CONSTRAINT job_views_pkey PRIMARY KEY (view_id),
  CONSTRAINT job_views_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.jobs(job_id),
  CONSTRAINT job_views_viewer_id_fkey FOREIGN KEY (viewer_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.jobs (
  job_id integer NOT NULL DEFAULT nextval('jobs_job_id_seq'::regclass),
  employer_id integer,
  title character varying NOT NULL,
  description text,
  location character varying,
  remote_type character varying CHECK (remote_type::text = ANY (ARRAY['remote'::character varying, 'hybrid'::character varying, 'on-site'::character varying]::text[])),
  salary_min numeric,
  salary_max numeric,
  seniority character varying,
  tags ARRAY,
  screening_questions jsonb,
  is_active boolean DEFAULT true,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT jobs_pkey PRIMARY KEY (job_id),
  CONSTRAINT jobs_employer_id_fkey FOREIGN KEY (employer_id) REFERENCES public.employers(employer_id)
);
CREATE TABLE public.learning_paths (
  path_id integer NOT NULL DEFAULT nextval('learning_paths_path_id_seq'::regclass),
  skill_id integer,
  provider character varying NOT NULL,
  course_name character varying NOT NULL,
  course_url text NOT NULL UNIQUE,
  estimated_duration_hours integer,
  CONSTRAINT learning_paths_pkey PRIMARY KEY (path_id),
  CONSTRAINT learning_paths_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id)
);
CREATE TABLE public.mentor_requests (
  request_id integer NOT NULL DEFAULT nextval('mentor_requests_request_id_seq'::regclass),
  candidate_id integer,
  mentor_id integer,
  match_reason text,
  status character varying DEFAULT 'Pending'::character varying,
  requested_at timestamp without time zone DEFAULT now(),
  CONSTRAINT mentor_requests_pkey PRIMARY KEY (request_id),
  CONSTRAINT mentor_requests_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id),
  CONSTRAINT mentor_requests_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.mentors(mentor_id)
);
CREATE TABLE public.mentor_skills (
  mentor_id integer NOT NULL,
  skill_id integer NOT NULL,
  CONSTRAINT mentor_skills_pkey PRIMARY KEY (mentor_id, skill_id),
  CONSTRAINT mentor_skills_mentor_id_fkey FOREIGN KEY (mentor_id) REFERENCES public.mentors(mentor_id),
  CONSTRAINT mentor_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(skill_id)
);
CREATE TABLE public.mentors (
  mentor_id integer NOT NULL DEFAULT nextval('mentors_mentor_id_seq'::regclass),
  user_id integer UNIQUE,
  headline character varying,
  is_available boolean DEFAULT true,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT mentors_pkey PRIMARY KEY (mentor_id),
  CONSTRAINT mentors_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.pipeline_notes (
  note_id integer NOT NULL DEFAULT nextval('pipeline_notes_note_id_seq'::regclass),
  application_id integer,
  author_id integer,
  note_text text NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT pipeline_notes_pkey PRIMARY KEY (note_id),
  CONSTRAINT pipeline_notes_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.applications(application_id),
  CONSTRAINT pipeline_notes_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(user_id)
);
CREATE TABLE public.pipeline_stages (
  stage_id integer NOT NULL DEFAULT nextval('pipeline_stages_stage_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT pipeline_stages_pkey PRIMARY KEY (stage_id)
);
CREATE TABLE public.resumes (
  resume_id integer NOT NULL DEFAULT nextval('resumes_resume_id_seq'::regclass),
  candidate_id integer,
  file_name character varying,
  file_type character varying,
  uploaded_at timestamp without time zone DEFAULT now(),
  parsed_title character varying,
  parsed_summary text,
  parsed_skills ARRAY,
  parsed_experience jsonb,
  parsed_education jsonb,
  virus_scan_passed boolean DEFAULT false,
  CONSTRAINT resumes_pkey PRIMARY KEY (resume_id),
  CONSTRAINT resumes_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(candidate_id)
);
CREATE TABLE public.screening_questions (
  id integer NOT NULL DEFAULT nextval('screening_questions_id_seq'::regclass),
  job_id integer,
  question text NOT NULL,
  CONSTRAINT screening_questions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.skills (
  skill_id integer NOT NULL DEFAULT nextval('skills_skill_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT skills_pkey PRIMARY KEY (skill_id)
);
CREATE TABLE public.users (
  user_id integer NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
  email character varying NOT NULL UNIQUE,
  password_hash character varying,
  oauth_provider character varying,
  role character varying NOT NULL CHECK (role::text = ANY (ARRAY['candidate'::character varying, 'employer'::character varying, 'admin'::character varying]::text[])),
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (user_id)
);
CREATE TABLE public.work_experiences (
  id integer NOT NULL DEFAULT nextval('work_experiences_id_seq'::regclass),
  integer integer,
  title character varying,
  primary key character varying NOT NULL,
  location character varying,
  start_date date,
  end_date date,
  description text,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT work_experiences_pkey PRIMARY KEY (id, primary key)
);