#!/usr/bin/env python3
"""Application Tracker CLI - Track your job applications

Usage:
    # Add new application
    python track_application.py add --company "Acme Corp" --role "Data Engineer" --salary "$160K" --resume resume_acme.docx
    
    # Update status
    python track_application.py update acme_corp --status interview --notes "Phone screen scheduled"
    
    # View pipeline
    python track_application.py list
    
    # View follow-ups due today
    python track_application.py follow-ups
    
    # View single application
    python track_application.py view acme_corp
"""

import sys
import argparse
from datetime import datetime

sys.path.insert(0, "C:/ecosystem")

from clawbot.skills.job_search.application_tracker import (
    ApplicationTracker, ApplicationStatus, print_application, print_pipeline_summary
)


def cmd_add(args):
    """Add a new application."""
    tracker = ApplicationTracker()
    
    print("=" * 60)
    print("ADD NEW APPLICATION")
    print("=" * 60)
    
    app = tracker.add_application(
        company=args.company,
        role=args.role,
        location=args.location or "Remote",
        salary_range=args.salary,
        resume_used=args.resume or "default",
        match_score=args.match or 0.0,
        contact_person=args.contact,
        contact_email=args.email,
        notes=args.notes
    )
    
    print(f"\n[OK] Application added successfully!")
    print(f"  ID: {app.id}")
    print(f"  Company: {app.company}")
    print(f"  Role: {app.role}")
    print(f"  Status: {app.status}")
    print(f"\n  Follow-up schedule:")
    for i, date in enumerate(app.follow_up_dates[:4], 1):
        print(f"    {i}. {date}")
    
    print(f"\n  Next action: Follow up on {app.follow_up_dates[0]}")
    print("=" * 60)


def cmd_update(args):
    """Update application status."""
    tracker = ApplicationTracker()
    
    # Find application by partial match
    app_id = args.app_id
    
    success = tracker.update_status(
        app_id=app_id,
        new_status=args.status,
        notes=args.notes
    )
    
    if success:
        print(f"[OK] Status updated to: {args.status.upper()}")
        if args.notes:
            print(f"  Notes added: {args.notes}")
    else:
        print(f"[ERROR] Could not find application: {app_id}")
        print("  Tip: Use 'list' command to see all applications")


def cmd_list(args):
    """List all applications."""
    tracker = ApplicationTracker()
    
    print("=" * 60)
    print("ALL APPLICATIONS")
    print("=" * 60)
    
    # Get report
    report = tracker.generate_pipeline_report()
    
    print(f"\nTotal: {report.get('total_applications', 0)} applications")
    print("\nBy Status:")
    
    status_order = [
        ApplicationStatus.OFFER.value,
        ApplicationStatus.ONSITE.value,
        ApplicationStatus.TECHNICAL_INTERVIEW.value,
        ApplicationStatus.PHONE_SCREEN.value,
        ApplicationStatus.APPLIED.value,
        ApplicationStatus.REJECTED.value,
        ApplicationStatus.GHOSTED.value
    ]
    
    for status in status_order:
        count = report.get('by_status', {}).get(status, 0)
        if count > 0 or args.all:
            status_label = status.replace("_", " ").upper()
            print(f"  {status_label}: {count}")
    
    print("\n[NOTE] Use 'view <app_id>' to see details of specific application")
    print("=" * 60)


def cmd_view(args):
    """View single application."""
    tracker = ApplicationTracker()
    
    app = tracker.get_application(args.app_id)
    
    if app:
        print_application(app)
    else:
        print(f"[ERROR] Application not found: {args.app_id}")
        print("  Tip: Use 'list' to see all application IDs")


def cmd_followups(args):
    """Show follow-ups due."""
    tracker = ApplicationTracker()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("=" * 60)
    print(f"FOLLOW-UPS DUE: {today}")
    print("=" * 60)
    
    # In full implementation, would query for applications
    # where today matches a follow-up date
    
    print("\n[Coming Soon] Daily follow-up reminders")
    print("  - Applications needing follow-up today")
    print("  - Email templates for follow-up messages")
    print("  - Auto-generated reminders")
    
    print("\n[MANUAL CHECK] Review applications with these follow-up dates:")
    print("  - Today")
    print("  - Past due")
    print("=" * 60)


def cmd_interactive():
    """Interactive mode - walk through adding application."""
    print("=" * 60)
    print("INTERACTIVE APPLICATION TRACKER")
    print("=" * 60)
    
    company = input("\nCompany name: ").strip()
    if not company:
        print("[ERROR] Company name required")
        return
    
    role = input("Role/Title: ").strip()
    if not role:
        print("[ERROR] Role required")
        return
    
    location = input("Location (default: Remote): ").strip() or "Remote"
    salary = input("Salary range (optional): ").strip() or None
    resume = input("Resume filename used (optional): ").strip() or "default"
    
    match_input = input("Match score 0-100 (optional): ").strip()
    match_score = float(match_input) if match_input else 0.0
    
    notes = input("Notes (optional): ").strip() or None
    
    # Add application
    tracker = ApplicationTracker()
    app = tracker.add_application(
        company=company,
        role=role,
        location=location,
        salary_range=salary,
        resume_used=resume,
        match_score=match_score,
        notes=notes
    )
    
    print(f"\n[OK] Application tracked!")
    print(f"  ID: {app.id}")
    print(f"  Follow up on: {app.follow_up_dates[0]}")


def main():
    parser = argparse.ArgumentParser(
        description="Track job applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add new application
  python track_application.py add --company "Acme" --role "Data Engineer"
  
  # Interactive mode (easiest)
  python track_application.py
  
  # List all applications
  python track_application.py list
  
  # View specific application
  python track_application.py view app_20260203_acme_data_engineer
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add new application')
    add_parser.add_argument('--company', required=True, help='Company name')
    add_parser.add_argument('--role', required=True, help='Job title/role')
    add_parser.add_argument('--location', default='Remote', help='Job location')
    add_parser.add_argument('--salary', help='Salary range')
    add_parser.add_argument('--resume', help='Resume filename used')
    add_parser.add_argument('--match', type=float, help='Match score 0-100')
    add_parser.add_argument('--contact', help='Contact person name')
    add_parser.add_argument('--email', help='Contact email')
    add_parser.add_argument('--notes', help='Additional notes')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update application status')
    update_parser.add_argument('app_id', help='Application ID (or partial match)')
    update_parser.add_argument('--status', required=True, 
                               choices=[s.value for s in ApplicationStatus],
                               help='New status')
    update_parser.add_argument('--notes', help='Update notes')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all applications')
    list_parser.add_argument('--all', action='store_true', help='Show all statuses including zero counts')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View specific application')
    view_parser.add_argument('app_id', help='Application ID')
    
    # Follow-ups command
    subparsers.add_parser('follow-ups', help='Show follow-ups due today')
    
    args = parser.parse_args()
    
    if not args.command:
        # Interactive mode
        cmd_interactive()
    elif args.command == 'add':
        cmd_add(args)
    elif args.command == 'update':
        cmd_update(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'view':
        cmd_view(args)
    elif args.command == 'follow-ups':
        cmd_followups(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
