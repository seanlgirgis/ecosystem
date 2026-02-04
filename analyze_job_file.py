#!/usr/bin/env python3
"""Analyze a job file from the pipeline inbox

Usage:
    python analyze_job_file.py inbox/00001.DATABRICKS.02042026.1213.md
    python analyze_job_file.py C:\ecosystem\jobPipeLine\inbox\00001.DATABRICKS.02042026.1213.md
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, "C:/ecosystem")

from clawbot.skills.job_search import JobSearchSkill, JobPosting
from datetime import datetime


def extract_job_description_from_file(file_path):
    """Extract job description from pipeline file format."""
    
    content = Path(file_path).read_text(encoding='utf-8')
    
    # Try to find original job description in the file
    # Look for common patterns
    
    # Pattern 1: Look for "Job Description:" or similar headers
    patterns = [
        r'(?:Job Description|About the Role|What You\'ll Do|Description):(.*?)(?=\n#{1,6}\s|$)',
        r'(?:Responsibilities|Requirements|Qualifications):(.*?)(?=\n#{1,6}\s|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # If no pattern found, return full content (minus the analysis headers)
    # Remove lines starting with ### or ** that are likely analysis
    lines = content.split('\n')
    job_lines = []
    for line in lines:
        # Skip analysis lines
        if line.startswith('🎯') or line.startswith('**Why') or line.startswith('**Required'):
            continue
        if 'Match Score:' in line or 'APPLY NOW' in line:
            continue
        job_lines.append(line)
    
    return '\n'.join(job_lines).strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_job_file.py <path_to_job_file>")
        print("Example: python analyze_job_file.py inbox/00001.DATABRICKS.02042026.1213.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        # Try relative to jobPipeLine
        alt_path = Path("C:/ecosystem/jobPipeLine") / file_path
        if alt_path.exists():
            file_path = str(alt_path)
        else:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
    
    print("=" * 70)
    print("RE-ANALYZING JOB FILE")
    print("=" * 70)
    print(f"File: {file_path}")
    print()
    
    # Extract job description
    job_description = extract_job_description_from_file(file_path)
    
    if not job_description or len(job_description) < 100:
        print("Warning: Could not extract clear job description.")
        print("Using full file content...")
        job_description = Path(file_path).read_text(encoding='utf-8')
    
    # Analyze
    print("Analyzing with AWS Bedrock (Kimi 2.5)...")
    print("-" * 70)
    
    skill = JobSearchSkill()
    
    # Get company/role from filename
    filename = Path(file_path).stem
    parts = filename.split('.')
    company = parts[1] if len(parts) > 1 else "Unknown"
    
    job = JobPosting(
        id=f"reanalysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title=f"Role at {company}",
        company=company,
        location="Unknown",
        description=job_description[:4000],  # Limit to save tokens
        url=f"file://{file_path}",
        source="job_file_reanalysis",
        posted_date=datetime.now().isoformat()
    )
    
    result = skill.process_job(job)
    
    # Display results
    print(f"\n[SCORE] MATCH: {result.match_score:.0f}%")
    print("-" * 70)
    
    if result.analysis:
        analysis = result.analysis
        
        print(f"\n[SKILLS] Required:")
        for skill_name in analysis.get('required_skills', [])[:10]:
            print(f"   - {skill_name}")
        
        print(f"\n[SALARY] {analysis.get('salary_range', 'Not specified')}")
        print(f"[WORK] {analysis.get('work_arrangement', 'Not specified')}")
        print(f"[EXP] {analysis.get('years_experience', 'Not specified')}")
        
        print(f"\n[ANALYSIS]")
        print(f"   {analysis.get('match_reasoning', 'N/A')}")
        
        if analysis.get('red_flags'):
            print(f"\n[RED FLAGS]")
            for flag in analysis.get('red_flags', []):
                print(f"   - {flag}")
        
        should_apply = analysis.get('should_apply', False)
        print("\n" + "=" * 70)
        if result.match_score >= 80 and should_apply:
            print("[APPLY NOW] High match - apply immediately")
        elif result.match_score >= 65:
            print("[CONSIDER] Good match - consider applying")
        elif result.match_score >= 50:
            print("[MAYBE] Stretch role - apply if interested")
        else:
            print("[SKIP] Low match - skip this one")
        print("=" * 70)
    
    print("\n[SAVED] Re-analysis stored in SecondBrain.")
    print(f"\nCompare with original analysis in file:")
    print(f"   Original score: (see file)")
    print(f"   New score: {result.match_score:.0f}%")


if __name__ == "__main__":
    main()
