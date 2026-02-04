"""Job Search CLI - Quick job analysis tool

Usage:
    python -m clawbot.skills.job_search.cli analyze "paste job description here"
    python -m clawbot.skills.job_search.cli daily-report
"""

import sys
import json
from datetime import datetime

sys.path.insert(0, "C:/ecosystem")

from clawbot.skills.job_search.job_scraper import JobSearchSkill, JobPosting
from secondbrain import recall


def analyze_job(description: str, title: str = "Unknown", company: str = "Unknown"):
    """Analyze a single job description."""
    
    print("=" * 60)
    print("JOB ANALYSIS")
    print("=" * 60)
    
    skill = JobSearchSkill()
    
    job = JobPosting(
        id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title=title,
        company=company,
        location="Unknown",
        description=description,
        url="manual_entry",
        source="user_input",
        posted_date=datetime.now().isoformat()
    )
    
    result = skill.process_job(job)
    
    print(f"\nJob: {result.title} at {result.company}")
    print(f"Match Score: {result.match_score:.1f}%")
    
    if result.analysis:
        print(f"\nRequired Skills: {', '.join(result.analysis.get('required_skills', []))}")
        print(f"Experience: {result.analysis.get('years_experience', 'N/A')}")
        print(f"Salary: {result.analysis.get('salary_range', 'N/A')}")
        print(f"Work Arrangement: {result.analysis.get('work_arrangement', 'N/A')}")
        print(f"\nReasoning: {result.analysis.get('match_reasoning', 'N/A')}")
        
        should_apply = result.analysis.get('should_apply', False)
        if result.match_score >= 75 and should_apply:
            print("\n🎯 RECOMMENDATION: APPLY NOW")
        elif result.match_score >= 60:
            print("\n🤔 RECOMMENDATION: CONSIDER APPLYING")
        else:
            print("\n❌ RECOMMENDATION: SKIP")
    
    print("\nStored in SecondBrain for tracking.")
    return result


def daily_report():
    """Show jobs analyzed today."""
    print("=" * 60)
    print("DAILY JOB SEARCH REPORT")
    print("=" * 60)
    print("\nFeature: Query SecondBrain for today's jobs")
    print("(Implementation: search knowledge base by date)")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m clawbot.skills.job_search.cli analyze 'job description'")
        print("  python -m clawbot.skills.job_search.cli daily-report")
        return
    
    command = sys.argv[1]
    
    if command == "analyze":
        if len(sys.argv) < 3:
            print("Error: Provide job description")
            return
        description = " ".join(sys.argv[2:])
        analyze_job(description)
    
    elif command == "daily-report":
        daily_report()
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
