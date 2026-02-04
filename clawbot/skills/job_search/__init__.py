"""Job Search Skill

Quick job analysis and matching.

Usage:
    from clawbot.skills.job_search import JobSearchSkill
    
    skill = JobSearchSkill()
    job = skill.process_job(job_posting)
    print(f"Match: {job.match_score}%")

Or CLI:
    python -m clawbot.skills.job_search.cli analyze "paste job description"
"""

from .job_scraper import JobSearchSkill, JobPosting, test_job_search

__all__ = ["JobSearchSkill", "JobPosting", "test_job_search"]
