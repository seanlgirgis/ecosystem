"""Job Search Skill - MVP for urgent job hunt

Scrapes job sites, analyzes with Bedrock, matches to skills, stores results.
"""

import json
import re
import time
import random
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, "C:/ecosystem")

import boto3
from secondbrain import remember, recall


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_date: str
    salary_range: Optional[str] = None
    match_score: float = 0.0
    analysis: Optional[dict] = None


class JobSearchSkill:
    """Skill for automated job searching and analysis."""
    
    SKILL_NAME = "job_search"
    SKILL_VERSION = "1.0.0"
    
    # AWS Bedrock config
    AWS_PROFILE = "study"
    AWS_REGION = "us-east-1"
    MODEL_ID = "moonshot.kimi-k2-thinking"
    
    def __init__(self):
        self.session = boto3.Session(profile_name=self.AWS_PROFILE)
        self.bedrock = self.session.client('bedrock-runtime', region_name=self.AWS_REGION)
        
        # Load skills for matching
        skills_data = recall("sean_girgis_skills_flat")
        self.skills = skills_data.get("value", []) if skills_data else []
        
    def analyze_job_with_ai(self, job_description: str, job_title: str) -> dict:
        """Use Bedrock to analyze job description."""
        
        prompt = f"""Analyze this job posting for a Data Engineer role.

Job Title: {job_title}
Job Description:
{job_description[:3000]}  # Truncate to save tokens

Your task:
1. Extract required technical skills (Python, AWS, PySpark, SQL, etc.)
2. Extract required years of experience
3. Extract salary range if mentioned
4. Identify if it's remote/hybrid/onsite
5. Rate match quality for someone with: Python, PySpark, AWS, ML Forecasting, 20 years experience

Respond in JSON format:
{{
    "required_skills": ["skill1", "skill2"],
    "years_experience": "5+ years",
    "salary_range": "$150K-$180K" or "Not specified",
    "work_arrangement": "remote/hybrid/onsite",
    "match_score": 85,
    "match_reasoning": "Brief explanation",
    "red_flags": ["any concerns"],
    "should_apply": true/false
}}"""

        try:
            body = {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.3
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.MODEL_ID,
                body=json.dumps(body)
            )
            
            result = json.loads(response['body'].read())
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '{}')
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"match_score": 50, "should_apply": False, "error": "Failed to parse"}
                
        except Exception as e:
            print(f"Bedrock analysis failed: {e}")
            return {"match_score": 50, "should_apply": False, "error": str(e)}
    
    def calculate_skill_match(self, required_skills: List[str]) -> float:
        """Calculate how many required skills Sean has."""
        if not required_skills or not self.skills:
            return 50.0
        
        sean_skills_lower = [s.lower() for s in self.skills]
        matches = 0
        
        for req_skill in required_skills:
            req_lower = req_skill.lower()
            if any(req_lower in sean_skill or sean_skill in req_lower for sean_skill in sean_skills_lower):
                matches += 1
        
        return (matches / len(required_skills)) * 100 if required_skills else 50.0
    
    def search_linkedin(self, keywords: str = "Data Engineer", location: str = "Remote") -> List[JobPosting]:
        """Search LinkedIn jobs."""
        # Placeholder - actual implementation needs Selenium/Playwright
        # For MVP, return empty list - will implement with browser automation
        print("LinkedIn search requires browser automation - implement with Selenium")
        return []
    
    def search_indeed(self, keywords: str = "Data Engineer", location: str = "Remote") -> List[JobPosting]:
        """Search Indeed jobs."""
        # Placeholder - actual implementation needs Selenium/Playwright
        print("Indeed search requires browser automation - implement with Selenium")
        return []
    
    def process_job(self, job: JobPosting) -> JobPosting:
        """Analyze job and calculate match score."""
        
        # Get AI analysis
        analysis = self.analyze_job_with_ai(job.description, job.title)
        job.analysis = analysis
        
        # Calculate match score
        ai_score = analysis.get("match_score", 50)
        skill_score = self.calculate_skill_match(analysis.get("required_skills", []))
        
        # Combined score (AI reasoning + skill overlap)
        job.match_score = (ai_score * 0.6) + (skill_score * 0.4)
        
        # Store in SecondBrain
        remember(
            key=f"job_{job.id}",
            value={
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "match_score": job.match_score,
                "analysis": analysis,
                "url": job.url,
                "date_found": datetime.now().isoformat()
            },
            metadata={
                "type": "job_posting",
                "source": job.source,
                "match_tier": "high" if job.match_score >= 75 else "medium" if job.match_score >= 60 else "low"
            }
        )
        
        return job
    
    def get_daily_recommendations(self, min_score: float = 75.0) -> List[dict]:
        """Get jobs to apply to today."""
        # Query all jobs from memory (simplified - in production would query vector DB)
        # For now, return a placeholder
        return []
    
    def generate_application_tracker(self) -> dict:
        """Generate tracker of all jobs and status."""
        return {
            "date": datetime.now().isoformat(),
            "jobs_found": 0,
            "jobs_applied": 0,
            "jobs_to_apply": []
        }


# Quick test function
def test_job_search():
    """Test the job search skill."""
    print("Testing Job Search Skill...")
    
    skill = JobSearchSkill()
    
    # Test job description analysis
    test_job = """
    Senior Data Engineer - Acme Corp
    
    We are looking for a Senior Data Engineer with 5+ years of experience
    in Python, PySpark, and AWS. You will build ETL pipelines, work with
    large datasets, and deploy ML models.
    
    Required:
    - Python, PySpark
    - AWS (S3, Glue, Athena)
    - SQL, PostgreSQL
    - 5+ years experience
    
    Nice to have:
    - Machine Learning
    - GenAI/LLM experience
    
    Salary: $160K-$190K
    Location: Remote (US)
    """
    
    job = JobPosting(
        id="test_001",
        title="Senior Data Engineer",
        company="Acme Corp",
        location="Remote",
        description=test_job,
        url="https://example.com/job",
        source="test",
        posted_date="2026-02-03"
    )
    
    result = skill.process_job(job)
    
    print(f"\nMatch Score: {result.match_score:.1f}%")
    print(f"Analysis: {json.dumps(result.analysis, indent=2)}")
    
    return result


if __name__ == "__main__":
    test_job_search()
