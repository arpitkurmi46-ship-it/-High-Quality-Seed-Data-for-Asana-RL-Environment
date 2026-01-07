import uuid
import random
import datetime
from simulator import simulate_task

FIRST_NAMES = [
    "Rahul", "Sneha", "Arjun", "Priya", "Amit", "Neha", "Rohan", "Anjali",
    "Vikram", "Isha", "Kabir", "Simran", "Aditya", "Pooja", "Nikhil", "Ayesha",
    "Karan", "Meera", "Siddharth", "Tanya", "Harsh", "Tara", "Sameer", "Ritika"
]

LAST_NAMES = [
    "Mehta", "Sharma", "Verma", "Gupta", "Agarwal", "Reddy",
    "Patel", "Khan", "Singh", "Das", "Chopra", "Bose", "Iyer",
    "Bhatt", "Sahu", "Yadav", "Nair", "Shetty", "Gill"
]


ROLES = ["Backend Engineer", "Frontend Engineer", "Product Manager", "Designer"]

def generate_users(n):
    roles = [
        "Engineer", "Engineer", "Engineer",
        "QA",
        "Designer",
        "Marketing",
        "Product Manager",
        "Operations"
    ]

    users = []
    for _ in range(n):
        user = {
            "user_id": str(uuid.uuid4()),
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "role": random.choice(roles)
        }
        users.append(user)

    return users


ENGINEERING_PROJECTS = [
    "Mobile App Revamp",
    "Backend API Modernization",
    "Authentication System Upgrade",
    "CI/CD Pipeline Improvements",
    "Database Migration Phase 1",
    "Infrastructure Monitoring Enhancement",
    "Search Feature Rollout",
    "Payment Gateway Integration",
    "Error Tracking and Logging Upgrade",
    "Performance Optimization Sprint"
]

MARKETING_PROJECTS = [
    "Q1 Product Launch",
    "Brand Awareness Campaign",
    "SEO Optimization Plan",
    "Email Funnel Improvement",
    "Landing Page Redesign",
    "Customer Webinar Series",
    "Lead Nurturing Campaign",
    "Social Media Blitz Week",
    "Partner Outreach Program",
    "Product Demo Video Production"
]

OPERATIONS_PROJECTS = [
    "Employee Onboarding Workflow",
    "Compliance Audit Preparation",
    "Vendor Contract Renewal",
    "IT Asset Inventory Update",
    "Customer Support Process Review",
    "Internal SOP Standardization",
    "Security Policy Update",
    "Budget Allocation Review",
    "Hiring Pipeline Management",
    "Quarterly Performance Review Setup"
]


def generate_projects(n, org_id, start_date):
    projects = []
    all_projects = ENGINEERING_PROJECTS + MARKETING_PROJECTS + OPERATIONS_PROJECTS

    for i in range(n):
        pname = random.choice(all_projects)

        projects.append({
            "project_id": str(uuid.uuid4()),
            "name": pname,
            "org_id": org_id,
            "start_date": start_date + datetime.timedelta(days=i * 5)
        })

    return projects

ENG_TASKS = [
    "Refactor authentication middleware",
    "Fix session timeout bug",
    "Improve database indexing for search",
    "Migrate API endpoints to v3",
    "Implement OAuth token refresh",
    "Optimize query latency",
    "Add pagination support",
    "Improve unit test coverage",
    "Fix UI rendering issue",
    "Integrate error monitoring tool"
]


MARKETING_TASKS = [
    "Write launch campaign email copy",
    "Design product landing page",
    "Prepare social media calendar",
    "Optimize blog SEO for keywords",
    "Coordinate influencer outreach",
    "Create ad graphics for launch",
    "Record promotional video script",
    "Draft customer success story",
    "Analyze lead conversion funnel",
    "Prepare webinar slide deck"
]


OPS_TASKS = [
    "Prepare employee onboarding checklist",
    "Renew cloud service contracts",
    "Audit system access permissions",
    "Prepare monthly uptime report",
    "Review vendor invoices",
    "Update internal documentation",
    "Schedule security patching",
    "Reconcile product inventory",
    "Verify compliance reports",
    "Review support ticket backlog"
]

