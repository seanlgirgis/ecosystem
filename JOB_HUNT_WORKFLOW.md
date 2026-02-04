# Job Hunt Workflow - Complete Guide

**Your daily workflow to land a job in 30 days.**

---

## Prerequisites (Done ✓)

- [x] AWS Bedrock configured (Kimi 2.5)
- [x] SecondBrain working (memory storage)
- [x] Job analyzer working (`analyze_job.py`)
- [x] Resume tailor working (`resume/tailor_resume.py`)
- [x] Application tracker working (`track_application.py`)

---

## Daily Workflow (30-60 minutes)

### Step 1: Find Jobs (15 min)

Search these sites in order:
1. **LinkedIn** - 10 jobs
2. **Indeed** - 10 jobs  
3. **Dice** - 5 jobs

**Target criteria:**
- Title: Data Engineer, ML Engineer, AI Engineer
- Location: Remote or Dallas/Hybrid
- Salary: $150K+

---

### Step 2: Analyze Each Job (15 min)

For each job found:

```powershell
cd C:\ecosystem

# Copy job description, then run:
python analyze_job.py "paste job description here"
```

**Output example:**
```
[SCORE] MATCH: 87%
[SKILLS] Python, PySpark, AWS, ML
[SALARY] $170K-$200K
[WORK] remote
[APPLY NOW] High match - apply immediately
```

**Decision:**
- **Match >= 75%:** Proceed to Step 3
- **Match 60-74%:** Consider (stretch role)
- **Match < 60%:** Skip

---

### Step 3: Generate Tailored Resume (10 min)

For high-match jobs (>= 75%):

```powershell
cd C:\ecosystem\resume

# Generate tailored resume
python tailor_resume.py \
  --job "paste same job description" \
  --company "Company Name" \
  --output resume_company_name
```

**Output:**
- `output/resume_company_name.docx` (Word - editable)
- `output/resume_company_name.html` (web view)
- `output/resume_company_name.md` (Markdown)

**Review the DOCX**, make any final edits.

---

### Step 4: Submit Application (10 min)

1. Apply on company website or LinkedIn
2. Upload tailored resume (DOCX or PDF)
3. **Track the application:**

```powershell
cd C:\ecosystem

# Track the application
python track_application.py add \
  --company "Company Name" \
  --role "Senior Data Engineer" \
  --salary "$170K-$200K" \
  --resume "resume_company_name.docx" \
  --match 87 \
  --notes "Applied via LinkedIn. High match."
```

**Output:**
```
[OK] Application added successfully!
  ID: app_20260203_company_name_senior_data_engineer
  Follow up on: 2026-02-10
```

---

### Step 5: Set Follow-up Reminder

The tracker automatically sets follow-up dates:
- Day 7
- Day 14
- Day 21
- Day 30

**Check daily:**
```powershell
python track_application.py follow-ups
```

---

## Weekly Summary

**Check your pipeline:**
```powershell
python track_application.py list
```

**View specific application:**
```powershell
python track_application.py view app_20260203_acme_data_engineer
```

**Update status when you hear back:**
```powershell
python track_application.py update app_20260203_acme_data_engineer \
  --status interview \
  --notes "Phone screen scheduled for Friday"
```

---

## Status Values

| Status | When to Use |
|--------|-------------|
| `applied` | Just submitted |
| `phone_screen` | Recruiter call scheduled/done |
| `technical_interview` | Coding/system design interview |
| `onsite` | Final round interviews |
| `offer` | Offer received! |
| `rejected` | Not moving forward |
| `ghosted` | No response after 30 days |

---

## Target Metrics (Per Week)

| Metric | Target |
|--------|--------|
| Jobs analyzed | 20 |
| Applications sent | 10-15 |
| High-match (>=75%) apps | 5-8 |
| Follow-ups sent | 5-7 |
| Phone screens | 2-3 |
| Technical interviews | 1-2 |

---

## Cost Per Application

| Step | Cost |
|------|------|
| Job analysis | $0.00007 |
| Resume tailoring | $0.0001 |
| Application tracking | $0 (local) |
| **Total per app** | **~$0.0002** |
| **100 applications** | **~$0.02** |

**Your $199 credits = ~1,000,000 applications** (you'll get a job first!)

---

## Quick Reference

### All Commands

```powershell
# Activate environment
cd C:\ecosystem
. .\env_setter.ps1

# Analyze job
python analyze_job.py "job description"

# Generate tailored resume
cd resume
python tailor_resume.py --job "description" --company "Name"

# Track application
cd C:\ecosystem
python track_application.py add --company "Name" --role "Role"

# List all applications
python track_application.py list

# View specific
python track_application.py view <app_id>

# Update status
python track_application.py update <app_id> --status interview

# Check follow-ups
python track_application.py follow-ups
```

---

## File Locations

| Output | Location |
|--------|----------|
| Tailored resumes | `C:\ecosystem\resume\output\` |
| Application data | SecondBrain (memory.pkl) |
| Your profile | `sean_girgis_skills_profile` |
| Git repo | https://github.com/seanlgirgis/ecosystem |

---

## Success Checklist

**Week 1:**
- [ ] 10 applications sent
- [ ] 5 high-match (>=75%)
- [ ] 3 follow-ups sent

**Week 2:**
- [ ] 20 total applications
- [ ] 1 phone screen scheduled
- [ ] Resume tailored for each application

**Week 3:**
- [ ] 30 total applications
- [ ] 3 phone screens completed
- [ ] 1 technical interview

**Week 4:**
- [ ] 40 total applications
- [ ] 5 phone screens
- [ ] 2 technical interviews
- [ ] 1 offer (GOAL!)

---

## Emergency Contacts

If stuck:
- AWS Console: https://console.aws.amazon.com/
- GitHub Repo: https://github.com/seanlgirgis/ecosystem
- Cost dashboard: https://console.aws.amazon.com/billing/

---

**Start now. Apply to your first job today.**
