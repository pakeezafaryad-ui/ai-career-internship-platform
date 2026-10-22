
import json

from services.database import SessionLocal, LearningRoadmap


def generate_learning_roadmap(
    target_career,
    current_skills=None,
    duration_weeks=8,
):
    """Generate a structured learning plan for a target career."""

    career_paths = {
        "AI Engineer": [
            ("Python fundamentals", "Practice variables, functions, and OOP."),
            ("Data analysis", "Learn NumPy, Pandas, and data cleaning."),
            ("Machine learning", "Study supervised and unsupervised learning."),
            ("AI applications", "Build a small AI application using an API."),
            ("Portfolio project", "Build, test, and document an AI project."),
        ],
        "Python Developer": [
            ("Python fundamentals", "Practice functions, collections, and files."),
            ("Object-oriented programming", "Practice classes and inheritance."),
            ("Git and GitHub", "Track code and publish projects."),
            ("APIs and databases", "Build an application using SQL and APIs."),
            ("Portfolio project", "Build and document a Python application."),
        ],
        "Data Analyst": [
            ("Excel", "Practice formulas, sorting, and pivot tables."),
            ("Statistics", "Study averages, variation, and distributions."),
            ("SQL", "Practice queries, filtering, and joins."),
            ("Python data analysis", "Use Pandas to clean and analyze data."),
            ("Portfolio dashboard", "Present findings using visualizations."),
        ],
        "Web Developer": [
            ("HTML", "Build accessible webpage structures."),
            ("CSS", "Practice layouts, responsive design, and styling."),
            ("JavaScript", "Learn functions, events, and DOM manipulation."),
            ("Backend and databases", "Build a simple API and database."),
            ("Portfolio website", "Deploy and document a website."),
        ],
        "Java Developer": [
            ("Java fundamentals", "Practice methods, arrays, and exceptions."),
            ("Object-oriented programming", "Practice classes, inheritance, and interfaces."),
            ("Data structures", "Learn lists, stacks, queues, and maps."),
            ("Databases and testing", "Practice SQL and unit testing."),
            ("Portfolio application", "Build and document a Java project."),
        ],
        "Cybersecurity Analyst": [
            ("Security fundamentals", "Learn confidentiality, integrity, and availability."),
            ("Networking", "Study IP addresses, DNS, and common protocols."),
            ("Linux basics", "Practice commands and file permissions."),
            ("Defensive security", "Learn logs, risk assessment, and incident response."),
            ("Security portfolio", "Document safe lab exercises and findings."),
        ],
        "Machine Learning Engineer": [
            ("Python and mathematics", "Practice Python, statistics, and linear algebra."),
            ("Data preparation", "Clean data and prepare useful features."),
            ("Machine learning", "Train and evaluate introductory models."),
            ("Model improvement", "Compare metrics and reduce overfitting."),
            ("Portfolio project", "Build and document a complete ML workflow."),
        ],
        "Full Stack Developer": [
            ("HTML and CSS", "Build responsive page layouts."),
            ("JavaScript", "Learn events, forms, and asynchronous code."),
            ("Frontend development", "Build reusable interface components."),
            ("Backend and databases", "Create APIs and connect a database."),
            ("Full stack project", "Build, test, and deploy a complete application."),
        ],
    }

    career = (target_career or "").strip()

    matched_career = next(
        (
            name for name in career_paths
            if name.casefold() == career.casefold()
        ),
        None,
    )

    if matched_career is None:
        return {
            "title": f"Learning Roadmap: {career or 'Career Exploration'}",
            "duration_weeks": duration_weeks,
            "current_skills": current_skills or [],
            "weeks": [],
            "message": "Please select a supported career.",
        }

    try:
        duration_weeks = int(duration_weeks)
    except (TypeError, ValueError):
        duration_weeks = 8

    duration_weeks = max(1, min(duration_weeks, 52))

    if isinstance(current_skills, str):
        current_skills = [
            item.strip()
            for item in current_skills.split(",")
            if item.strip()
        ]

    current_skills = current_skills or []

    modules = career_paths[matched_career]
    weeks = []

    # Distribute learning modules across the requested duration.
    for index, (topic, task) in enumerate(modules):
        start_week = (index * duration_weeks) // len(modules) + 1
        end_week = (
            ((index + 1) * duration_weeks) // len(modules)
        )
        end_week = max(start_week, end_week)

        weeks.append({
            "week": start_week,
            "end_week": end_week,
            "topic": topic,
            "task": task,
            "completed": False,
        })

    return {
        "title": f"{matched_career} Learning Roadmap",
        "career": matched_career,
        "duration_weeks": duration_weeks,
        "current_skills": current_skills,
        "weeks": weeks,
        "message": (
            "Follow the plan at your own pace and adjust it "
            "to your experience and available study time."
        ),
    }


def save_roadmap(user_id, roadmap):
    """Save a roadmap belonging to the logged-in user."""

    if not isinstance(roadmap, dict) or not roadmap.get("title"):
        return False

    db = SessionLocal()

    try:
        record = LearningRoadmap(
            user_id=user_id,
            title=roadmap["title"],
            plan_json=json.dumps(roadmap),
            progress_percent=0,
        )

        db.add(record)
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False

    finally:
        db.close()


def get_user_roadmaps(user_id):
    """Retrieve only roadmaps owned by the specified user."""

    db = SessionLocal()

    try:
        records = (
            db.query(LearningRoadmap)
            .filter(LearningRoadmap.user_id == user_id)
            .order_by(LearningRoadmap.id.desc())
            .all()
        )

        roadmaps = []

        for record in records:
            try:
                plan = json.loads(record.plan_json)
            except (json.JSONDecodeError, TypeError):
                plan = {}

            roadmaps.append({
                "id": record.id,
                "title": record.title,
                "plan": plan,
                "progress_percent": record.progress_percent,
            })

        return roadmaps

    finally:
        db.close()
