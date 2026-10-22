
def analyze_skill_gap(current_skills, target_career):
    """
    Compare a user's current skills with the skills
    recommended for their target career.
    """

    career_skills = {
        "Python Developer": [
            "Python",
            "Object-Oriented Programming",
            "Git and GitHub",
            "SQL",
            "REST APIs",
            "Testing",
        ],
        "AI Engineer": [
            "Python",
            "Machine Learning",
            "Data Analysis",
            "NumPy",
            "Pandas",
            "Deep Learning",
            "APIs",
        ],
        "Data Analyst": [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Visualization",
            "Pandas",
        ],
        "Web Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "Git and GitHub",
            "REST APIs",
            "SQL",
        ],
        "Java Developer": [
            "Java",
            "Object-Oriented Programming",
            "Data Structures",
            "SQL",
            "Git and GitHub",
            "Testing",
        ],
        "Cybersecurity Analyst": [
            "Networking",
            "Linux",
            "Python",
            "Security Fundamentals",
            "Risk Assessment",
            "Incident Response",
        ],
        "Machine Learning Engineer": [
            "Python",
            "Statistics",
            "Linear Algebra",
            "Machine Learning",
            "Data Processing",
            "Model Evaluation",
        ],
        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "SQL",
            "REST APIs",
            "Git and GitHub",
        ],
    }

    # Normalize skills for case-insensitive comparison
    if isinstance(current_skills, str):
        current_skills = current_skills.split(",")

    normalized_skills = {
        skill.strip().casefold()
        for skill in (current_skills or [])
        if isinstance(skill, str) and skill.strip()
    }

    target_career = (target_career or "").strip()

    # Find the closest matching career title
    matched_career = next(
        (
            career
            for career in career_skills
            if career.casefold() == target_career.casefold()
        ),
        None,
    )

    if matched_career is None:
        return {
            "target_career": target_career,
            "current_skills": sorted(normalized_skills),
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percent": 0,
            "message": (
                "Career not found. Please select a supported "
                "career from the platform."
            ),
        }

    required_skills = career_skills[matched_career]

    matched_skills = [
        skill
        for skill in required_skills
        if skill.casefold() in normalized_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.casefold() not in normalized_skills
    ]

    match_percent = round(
        len(matched_skills) / len(required_skills) * 100
    )

    return {
        "target_career": matched_career,
        "current_skills": sorted(normalized_skills),
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percent": match_percent,
        "message": (
            "Great start! Keep building your skills."
            if not missing_skills
            else "Focus on learning the missing skills "
                 "to prepare for this career."
        ),
    }
