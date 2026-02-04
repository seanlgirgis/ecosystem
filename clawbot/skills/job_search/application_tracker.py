"""Application Tracker - Track job applications and follow-ups

Stores applications in SecondBrain with status tracking and reminders.
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import sys

sys.path.insert(0, "C:/ecosystem")

from secondbrain import remember, recall, search_knowledge


class ApplicationStatus(Enum):
    APPLIED = "applied"
    PHONE_SCREEN = "phone_screen"
    TECHNICAL_INTERVIEW = "technical_interview"
    ONSITE = "onsite"
    OFFER = "offer"
    REJECTED = "rejected"
    GHOSTED = "ghosted"  # No response after 30 days
    WITHDRAWN = "withdrawn"


@dataclass
class JobApplication:
    id: str
    company: str
    role: str
    location: str
    salary_range: Optional[str]
    date_applied: str
    status: str
    resume_used: str
    match_score: float
    job_description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    notes: Optional[str] = None
    follow_up_dates: List[str] = None
    last_updated: str = None
    
    def __post_init__(self):
        if self.follow_up_dates is None:
            self.follow_up_dates = []
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()


class ApplicationTracker:
    """Track job applications with status and reminders."""
    
    SKILL_NAME = "application_tracker"
    SKILL_VERSION = "1.0.0"
    
    # Follow-up schedule (days after application)
    FOLLOW_UP_SCHEDULE = [7, 14, 21, 30]
    
    def __init__(self):
        self.applications = []
    
    def _generate_id(self, company: str, role: str) -> str:
        """Generate unique ID for application."""
        timestamp = datetime.now().strftime("%Y%m%d")
        company_clean = company.lower().replace(" ", "_")[:20]
        role_clean = role.lower().replace(" ", "_")[:20]
        return f"app_{timestamp}_{company_clean}_{role_clean}"
    
    def add_application(
        self,
        company: str,
        role: str,
        location: str = "Remote",
        salary_range: Optional[str] = None,
        resume_used: str = "default",
        match_score: float = 0.0,
        job_description: Optional[str] = None,
        contact_person: Optional[str] = None,
        contact_email: Optional[str] = None,
        notes: Optional[str] = None
    ) -> JobApplication:
        """Add a new job application."""
        
        app_id = self._generate_id(company, role)
        date_applied = datetime.now().isoformat()
        
        # Calculate follow-up dates
        follow_ups = []
        for days in self.FOLLOW_UP_SCHEDULE:
            follow_up_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            follow_ups.append(follow_up_date)
        
        application = JobApplication(
            id=app_id,
            company=company,
            role=role,
            location=location,
            salary_range=salary_range,
            date_applied=date_applied,
            status=ApplicationStatus.APPLIED.value,
            resume_used=resume_used,
            match_score=match_score,
            job_description=job_description[:500] if job_description else None,
            contact_person=contact_person,
            contact_email=contact_email,
            notes=notes,
            follow_up_dates=follow_ups
        )
        
        # Store in SecondBrain
        remember(
            key=f"application_{app_id}",
            value=asdict(application),
            metadata={
                "type": "job_application",
                "company": company,
                "status": ApplicationStatus.APPLIED.value,
                "date_applied": date_applied
            }
        )
        
        return application
    
    def update_status(self, app_id: str, new_status: str, notes: Optional[str] = None) -> bool:
        """Update application status."""
        
        # Retrieve existing application
        data = recall(f"application_{app_id}")
        if not data:
            print(f"Application not found: {app_id}")
            return False
        
        app_data = data.get("value", {})
        app_data["status"] = new_status
        app_data["last_updated"] = datetime.now().isoformat()
        
        if notes:
            existing_notes = app_data.get("notes", "")
            app_data["notes"] = f"{existing_notes}\n{datetime.now().strftime('%Y-%m-%d')}: {notes}".strip()
        
        # Store updated application
        remember(
            key=f"application_{app_id}",
            value=app_data,
            metadata={
                "type": "job_application",
                "company": app_data.get("company"),
                "status": new_status,
                "date_applied": app_data.get("date_applied")
            }
        )
        
        return True
    
    def get_follow_ups_due(self) -> List[Dict]:
        """Get applications needing follow-up today."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Search for applications with follow-up dates
        # This is a simplified version - in production would query more efficiently
        results = []
        
        # Get all applications from memory (simplified)
        # In practice, would search by metadata
        for key in ["application_status", "follow_up"]:
            try:
                data = recall(key)
                if data:
                    results.append(data)
            except:
                pass
        
        return results
    
    def generate_pipeline_report(self) -> Dict:
        """Generate pipeline overview report."""
        
        # Query all applications (simplified)
        applications = []
        
        # In production, would search SecondBrain for all application_* keys
        # For now, return template
        
        status_counts = {status.value: 0 for status in ApplicationStatus}
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_applications": 0,
            "by_status": status_counts,
            "active_applications": [],
            "follow_ups_today": [],
            "recent_activity": []
        }
        
        return report
    
    def get_application(self, app_id: str) -> Optional[Dict]:
        """Get single application by ID."""
        data = recall(f"application_{app_id}")
        return data.get("value") if data else None


# CLI helper functions
def print_application(app: Dict):
    """Pretty print application details."""
    print("\n" + "=" * 60)
    print(f"  {app.get('company')} - {app.get('role')}")
    print("=" * 60)
    print(f"  Location: {app.get('location', 'N/A')}")
    print(f"  Salary: {app.get('salary_range', 'Not disclosed')}")
    print(f"  Status: {app.get('status', 'N/A').upper()}")
    print(f"  Match Score: {app.get('match_score', 0)}%")
    print(f"  Date Applied: {app.get('date_applied', 'N/A')[:10]}")
    print(f"  Resume Used: {app.get('resume_used', 'default')}")
    
    if app.get('contact_person'):
        print(f"  Contact: {app.get('contact_person')}")
    if app.get('contact_email'):
        print(f"  Email: {app.get('contact_email')}")
    
    follow_ups = app.get('follow_up_dates', [])
    if follow_ups:
        print(f"  Follow-ups: {', '.join(follow_ups[:3])}")
    
    if app.get('notes'):
        print(f"\n  Notes:\n  {app.get('notes')[:200]}...")
    
    print("=" * 60)


def print_pipeline_summary(report: Dict):
    """Print pipeline summary."""
    print("\n" + "=" * 60)
    print("  APPLICATION PIPELINE")
    print("=" * 60)
    print(f"\n  Total Applications: {report.get('total_applications', 0)}")
    print("\n  By Status:")
    for status, count in report.get('by_status', {}).items():
        if count > 0:
            print(f"    {status}: {count}")
    print("=" * 60)


if __name__ == "__main__":
    # Test
    tracker = ApplicationTracker()
    
    # Add test application
    app = tracker.add_application(
        company="Test Corp",
        role="Senior Data Engineer",
        location="Remote",
        salary_range="$160K-$190K",
        resume_used="resume_test_corp.docx",
        match_score=85.0,
        notes="Applied via LinkedIn. Need to follow up in 7 days."
    )
    
    print(f"Added application: {app.id}")
    print_application(asdict(app))
