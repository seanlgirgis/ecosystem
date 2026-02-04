"""Job Search Skill

Job search, analysis, and application tracking.

Components:
- job_scraper.py: Job analysis and matching
- application_tracker.py: Application tracking and pipeline management
- cli.py: Command-line interface

Usage:
    from clawbot.skills.job_search import JobSearchSkill, ApplicationTracker
    
    # Analyze job
    skill = JobSearchSkill()
    job = skill.process_job(job_posting)
    
    # Track application
    tracker = ApplicationTracker()
    app = tracker.add_application(company="Acme", role="Data Engineer", ...)

CLI Commands:
    python -m clawbot.skills.job_search.cli analyze "job description"
    python track_application.py add --company "Acme" --role "Data Engineer"
"""

from .job_scraper import JobSearchSkill, JobPosting, test_job_search
from .application_tracker import (
    ApplicationTracker, 
    JobApplication, 
    ApplicationStatus,
    print_application,
    print_pipeline_summary
)

__all__ = [
    "JobSearchSkill", 
    "JobPosting", 
    "test_job_search",
    "ApplicationTracker",
    "JobApplication",
    "ApplicationStatus",
    "print_application",
    "print_pipeline_summary"
]
