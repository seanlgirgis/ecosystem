#!/usr/bin/env python3
"""Resume Tailor - AI-powered job-specific resume generation

Analyzes job description, selects relevant experience, generates tailored resume.

Usage:
    python tailor_resume.py --job "paste job description" --company "Acme Corp"
    python tailor_resume.py --job-file job.txt --company "Acme Corp" --output "acme_resume"
"""

import yaml
import json
import re
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, "C:/ecosystem")

from secondbrain import recall
from clawbot.skills.job_search import JobSearchSkill


def analyze_job_simple(description):
    """Simple keyword-based analysis (fallback if no Bedrock)."""
    description_lower = description.lower()
    
    # Keyword matching
    skills_found = []
    skill_keywords = {
        'python': ['python', 'pandas', 'numpy'],
        'pyspark': ['pyspark', 'spark', 'apache spark'],
        'aws': ['aws', 'amazon web services', 's3', 'glue', 'athena', 'lambda'],
        'sql': ['sql', 'postgresql', 'mysql', 'oracle', 'database'],
        'etl': ['etl', 'data pipeline', 'airflow', 'dag'],
        'ml': ['machine learning', 'ml', 'scikit-learn', 'prophet', 'forecasting'],
        'genai': ['genai', 'llm', 'openai', 'claude', 'bedrock'],
        'docker': ['docker', 'kubernetes', 'container'],
        'performance': ['apm', 'performance', 'monitoring', 'capacity']
    }
    
    for skill, keywords in skill_keywords.items():
        if any(kw in description_lower for kw in keywords):
            skills_found.append(skill)
    
    # Experience level
    exp_match = re.search(r'(\d+)\+?\s*years?', description, re.IGNORECASE)
    years_required = exp_match.group(1) if exp_match else "Not specified"
    
    # Salary
    salary_match = re.search(r'\$(\d+)[Kk]?\s*[-–]\s*\$(\d+)[Kk]?', description)
    salary_range = f"${salary_match.group(1)}K-${salary_match.group(2)}K" if salary_match else "Not specified"
    
    # Work type
    if 'remote' in description_lower:
        work_type = "remote"
    elif 'hybrid' in description_lower:
        work_type = "hybrid"
    elif 'onsite' in description_lower or 'on-site' in description_lower:
        work_type = "onsite"
    else:
        work_type = "not specified"
    
    return {
        'required_skills': skills_found,
        'years_experience': years_required,
        'salary_range': salary_range,
        'work_arrangement': work_type,
        'focus_areas': list(set(skills_found))[:5]  # Top 5
    }


def select_relevant_experience(store_data, job_analysis):
    """Select most relevant experience blocks from store."""
    
    required_skills = set(job_analysis.get('required_skills', []))
    
    # Score each experience block
    scored_experiences = []
    
    # CITI experience (always strong)
    if 'exp_citi_consultant' in store_data:
        citi = store_data['exp_citi_consultant']
        citi_text = str(citi).lower()
        score = sum(1 for skill in required_skills if skill in citi_text)
        scored_experiences.append(('exp_citi_consultant', score + 10))  # +10 for recency
    
    # G6 experience
    if 'exp_ca_consultant' in store_data:
        ca = store_data['exp_ca_consultant']
        ca_text = str(ca).lower()
        score = sum(1 for skill in required_skills if skill in ca_text)
        scored_experiences.append(('exp_ca_consultant', score + 5))
    
    # Sort by score
    scored_experiences.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 3-4
    return [key for key, score in scored_experiences[:4]]


def generate_tailored_layout(store_data, job_analysis, selected_experiences, company_name):
    """Generate a tailored resume layout YAML."""
    
    # Base structure
    layout = {
        'config': {
            'title': f"Resume for {company_name}",
            'generated_at': datetime.now().isoformat(),
            'tailored_for': company_name,
            'focus_skills': job_analysis.get('required_skills', [])
        },
        'sections': []
    }
    
    # Header
    layout['sections'].append({
        'type': 'header',
        'config': {'content_key': 'header_resume_sean'}
    })
    
    # Contact
    layout['sections'].append({
        'type': 'contact',
        'config': {'content_key': 'contact_info_main'}
    })
    
    # Summary - tailored
    if 'summary_data_eng' in store_data:
        layout['sections'].append({
            'type': 'summary',
            'config': {
                'content_key': 'summary_data_eng',
                'highlight_skills': job_analysis.get('required_skills', [])
            }
        })
    
    # Selected experiences (in priority order)
    for exp_key in selected_experiences:
        layout['sections'].append({
            'type': 'experience',
            'config': {'content_key': exp_key}
        })
    
    # Skills matrix
    layout['sections'].append({
        'type': 'skills_matrix',
        'config': {'content_key': 'core_ml_pillars'}
    })
    
    # Projects (select relevant ones)
    if 'proj_cloud_intelligence' in store_data:
        if any(s in ['aws', 'etl', 'genai'] for s in job_analysis.get('required_skills', [])):
            layout['sections'].append({
                'type': 'project',
                'config': {'content_key': 'proj_cloud_intelligence'}
            })
    
    if 'proj_predictive_pipeline' in store_data:
        if any(s in ['python', 'ml', 'forecasting'] for s in job_analysis.get('required_skills', [])):
            layout['sections'].append({
                'type': 'project',
                'config': {'content_key': 'proj_predictive_pipeline'}
            })
    
    return layout


def main():
    parser = argparse.ArgumentParser(description="Tailor resume for specific job")
    parser.add_argument('--job', help='Job description text')
    parser.add_argument('--job-file', help='File containing job description')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--output', default='tailored', help='Output filename')
    parser.add_argument('--use-bedrock', action='store_true', help='Use AWS Bedrock for analysis')
    args = parser.parse_args()
    
    print("=" * 70)
    print("RESUME TAILOR")
    print("=" * 70)
    print(f"\nTailoring for: {args.company}")
    
    # Get job description
    if args.job_file:
        with open(args.job_file, 'r') as f:
            job_description = f.read()
    elif args.job:
        job_description = args.job
    else:
        print("Error: Provide --job or --job-file")
        return
    
    # Analyze job
    print("\n[1] Analyzing job description...")
    if args.use_bedrock:
        skill = JobSearchSkill()
        job = type('Job', (), {'description': job_description, 'title': 'Unknown'})
        result = skill.analyze_job_with_ai(job_description, "Unknown")
        job_analysis = result
    else:
        job_analysis = analyze_job_simple(job_description)
    
    print(f"   Required skills: {', '.join(job_analysis.get('required_skills', []))}")
    print(f"   Experience: {job_analysis.get('years_experience', 'N/A')}")
    print(f"   Work type: {job_analysis.get('work_arrangement', 'N/A')}")
    
    # Load store
    print("\n[2] Loading experience database...")
    base_dir = Path(__file__).parent
    store_path = base_dir / 'data' / 'store.yaml'
    store_data = yaml.safe_load(open(store_path, 'r')) if store_path.exists() else {}
    
    # Select relevant experience
    print("\n[3] Selecting relevant experience...")
    selected = select_relevant_experience(store_data, job_analysis)
    print(f"   Selected: {', '.join(selected)}")
    
    # Generate tailored layout
    print("\n[4] Generating tailored layout...")
    layout = generate_tailored_layout(store_data, job_analysis, selected, args.company)
    
    # Save layout
    layout_path = base_dir / 'data' / f'resume_tailored_{args.company.lower().replace(" ", "_")}.yaml'
    with open(layout_path, 'w') as f:
        yaml.dump(layout, f, default_flow_style=False, allow_unicode=True)
    print(f"   Saved: {layout_path}")
    
    # Generate resume
    print("\n[5] Generating resume files...")
    import subprocess
    result = subprocess.run([
        sys.executable,
        str(base_dir / 'generate.py'),
        '--target', f'resume_tailored_{args.company.lower().replace(" ", "_")}',
        '--output', args.output
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return
    
    # Summary
    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)
    print(f"\nTailored for: {args.company}")
    print(f"Focus skills: {', '.join(job_analysis.get('required_skills', [])[:5])}")
    print(f"\nOutput files in: {base_dir}/output/")
    print(f"  - {args.output}.docx  (Word - for editing)")
    print(f"  - {args.output}.pdf   (PDF - for submission)")
    print(f"  - {args.output}.html  (Web view)")
    print(f"\nNext steps:")
    print(f"  1. Review {args.output}.docx")
    print("  2. Edit if needed")
    print("  3. Submit {args.output}.pdf with application")


if __name__ == "__main__":
    main()
