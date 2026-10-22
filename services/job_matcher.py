
import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "sample_jobs.json"
)


def load_jobs():
    """Load opportunities from the project's sample dataset."""

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            jobs = json.load(file)

        if not isinstance(jobs, list):
            return []

        return [
            job for job in jobs
            if isinstance(job, dict)
        ]

    except (OSError, json.JSONDecodeError):
        return []


def match_jobs(user_skills, target_role=None):
    """
    Rank sample opportunities by skill overlap.

    This is a basic matching score, not a hiring probability.
    """

    if isinstance(user_skills, str):
        user_skills = user_skills.split(",")

    normalized_skills = {
        skill.strip().casefold()
        for skill in (user_skills or [])
        if isinstance(skill, str) and skill.strip()
    }

    target_role = (target_role or "").strip().casefold()
    opportunities = load_jobs()
    results = []

    for job in opportunities:
        title = str(job.get("title", "Opportunity"))
        company = str(job.get("company", "Sample Organization"))
        description = str(job.get("description", ""))
        required_skills = job.get("skills", [])

        if isinstance(required_skills, str):
            required_skills = required_skills.split(",")

        required_skills = [
            skill.strip()
            for skill in required_skills
            if isinstance(skill, str) and skill.strip()
        ]

        # Optionally prioritize a requested role.
        role_text = title.casefold()

        if target_role and target_role not in role_text:
            # Keep other opportunities available, but rank them lower.
            role_matches = False
        else:
            role_matches = True

        matched_skills = [
            skill for skill in required_skills
            if skill.casefold() in normalized_skills
        ]

        if required_skills:
            match_percent = round(
                len(matched_skills) / len(required_skills) * 100
            )
        else:
            match_percent = 0

        results.append({
            "title": title,
            "company": company,
            "description": description,
            "skills": required_skills,
            "matched_skills": matched_skills,
            "missing_skills": [
                skill for skill in required_skills
                if skill.casefold() not in normalized_skills
            ],
            "match_percent": match_percent,
            "role_matches": role_matches,
            "source_type": job.get("source_type", "sample"),
            "application_url": job.get("application_url", ""),
        })

    results.sort(
        key=lambda item: (
            item["role_matches"],
            item["match_percent"],
        ),
        reverse=True,
    )

    return results

