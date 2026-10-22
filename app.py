"""Career recommendations based on interests, skills, and goals."""

CAREERS = {
    "AI Engineer": {
        "keywords": ["ai", "artificial intelligence", "machine learning", "automation"],
        "skills": ["Python", "Machine Learning", "Statistics", "Data Analysis"],
        "description": "Build intelligent applications, AI assistants, and machine-learning systems.",
        "next_step": "Learn Python, NumPy, pandas, and machine-learning fundamentals.",
    },
    "Python Developer": {
        "keywords": ["python", "programming", "software", "backend", "development"],
        "skills": ["Python", "OOP", "Git and GitHub", "APIs"],
        "description": "Build software, automation tools, APIs, and backend applications.",
        "next_step": "Build a Python project and learn APIs, testing, and databases.",
    },
    "Web Developer": {
        "keywords": ["web", "website", "frontend", "backend", "html", "css"],
        "skills": ["HTML", "CSS", "JavaScript", "Git and GitHub"],
        "description": "Create websites and interactive web applications.",
        "next_step": "Build a responsive website using HTML, CSS, and JavaScript.",
    },
    "Data Analyst": {
        "keywords": ["data", "analytics", "statistics", "visualization"],
        "skills": ["Python", "SQL", "Excel", "Data Visualization"],
        "description": "Turn data into useful insights, reports, and dashboards.",
        "next_step": "Practice SQL, spreadsheets, pandas, and data visualization.",
    },
    "Cybersecurity Analyst": {
        "keywords": ["cybersecurity", "security", "network", "ethical hacking"],
        "skills": ["Networking", "Linux", "Security Fundamentals", "Python"],
        "description": "Help organizations protect systems, networks, and information.",
        "next_step": "Study networking, Linux, and defensive security fundamentals.",
    },
    "Java Developer": {
        "keywords": ["java", "object oriented", "oop", "software development"],
        "skills": ["Java", "OOP", "SQL", "Git and GitHub"],
        "description": "Develop applications and software systems using Java.",
        "next_step": "Practice OOP, collections, SQL, and a complete Java project.",
    },
    "UI/UX Designer": {
        "keywords": ["design", "graphic design", "ui", "ux", "creative"],
        "skills": ["UI Design", "UX Research", "Prototyping", "Figma"],
        "description": "Design clear, attractive, and easy-to-use digital products.",
        "next_step": "Learn Figma and create a prototype for a simple application.",
    },
}


def _normalise_items(value):
    if isinstance(value, list):
        items = value
    else:
        items = str(value or "").replace(";", ",").split(",")

    return [str(item).strip().lower() for item in items if str(item).strip()]


def recommend_careers(interests, skills, career_goal=""):
    interest_items = _normalise_items(interests)
    skill_items = _normalise_items(skills)
    goal = str(career_goal or "").strip().lower()

    interest_text = " ".join(interest_items)
    results = []

    for career, details in CAREERS.items():
        keywords = [word.lower() for word in details["keywords"]]
        required = details["skills"]

        matched_skills = [
            skill for skill in required
            if any(
                user_skill == skill.lower()
                or user_skill in skill.lower()
                or skill.lower() in user_skill
                for user_skill in skill_items
            )
        ]

        matched_interests = [
            keyword for keyword in keywords
            if keyword in interest_text
        ]

        goal_match = bool(
            goal and (
                goal == career.lower()
                or career.lower() in goal
                or goal in career.lower()
            )
        )

        # Skills carry the most weight; interests and goals also contribute.
        score = round(
            (len(matched_skills) / max(len(required), 1)) * 60
            + min(len(matched_interests), 3) * 10
            + (20 if goal_match else 0)
        )
        score = min(score, 100)

        # Do not show unrelated careers just to fill the list.
        if score == 0:
            continue

        reasons = []
        if goal_match:
            reasons.append("It matches your stated career goal.")
        if matched_interests:
            reasons.append(
                "Related interests: " + ", ".join(matched_interests[:3]) + "."
            )
        if matched_skills:
            reasons.append(
                "You already have relevant skills: "
                + ", ".join(matched_skills) + "."
            )

        missing_skills = [
            skill for skill in required
            if skill not in matched_skills
        ]

        results.append({
            "career": career,
            "title": career,
            "description": details["description"],
            "score": score,
            "reason": " ".join(reasons) or (
                "This career may be worth exploring based on your profile."
            ),
            "skills": required,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "next_step": details["next_step"],
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:4]
