#!/usr/bin/env python3
"""Quick job analyzer - paste job description, get match score.

Usage:
    python analyze_job.py "paste job description here"

Or interactive:
    python analyze_job.py
    # Then paste description and press Enter
"""

import sys
sys.path.insert(0, "C:/ecosystem")

from clawbot.skills.job_search import JobSearchSkill, JobPosting
from datetime import datetime


def main():
    print("=" * 70)
    print("  JOB ANALYZER - Paste job description to get match score")
    print("=" * 70)
    print()
    
    # Get job description
    if len(sys.argv) > 1:
        description = " ".join(sys.argv[1:])
    else:
        print("Paste job description (press Enter twice when done):")
        lines = []
        while True:
            try:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            except EOFError:
                break
        description = "\n".join(lines)
    
    if not description.strip():
        print("No description provided.")
        return
    
    # Analyze
    print("\nAnalyzing with AWS Bedrock (Kimi K2.5)...")
    print("-" * 70)
    
    skill = JobSearchSkill()
    
    job = JobPosting(
        id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        title="Job Posting",
        company="Unknown",
        location="Unknown",
        description=description,
        url="manual_analysis",
        source="cli",
        posted_date=datetime.now().isoformat()
    )
    
    result = skill.process_job(job)
    
    # Display results
    print(f"\n[SCORE] MATCH: {result.match_score:.0f}%")
    print("-" * 70)
    
    if result.analysis:
        analysis = result.analysis
        
        print(f"\n[SKILLS] Required:")
        for skill in analysis.get('required_skills', [])[:10]:
            print(f"   • {skill}")
        
        print(f"\n[SALARY] {analysis.get('salary_range', 'Not specified')}")
        print(f"[WORK] {analysis.get('work_arrangement', 'Not specified')}")
        print(f"[EXP] {analysis.get('years_experience', 'Not specified')}")
        
        print(f"\n[ANALYSIS]")
        print(f"   {analysis.get('match_reasoning', 'N/A')}")
        
        if analysis.get('red_flags'):
            print(f"\n[RED FLAGS]")
            for flag in analysis.get('red_flags', []):
                print(f"   • {flag}")
        
        # Recommendation
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
    
    print("\n[SAVED] Result stored in SecondBrain.")
    print("\nNext steps:")
    print("  1. If score >= 75%: Tailor resume and apply")
    print("  2. Track application: remember(key='applied_acme', value={...})")
    print("  3. Set follow-up reminder")


if __name__ == "__main__":
    main()
