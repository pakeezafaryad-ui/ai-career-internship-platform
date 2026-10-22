```python
"""
Career Advisor Service
Recommends career paths based on interests, skills, and career goals.
"""


CAREER_DATA = {
    "AI Engineer": {
        "keywords": ["ai", "artificial intelligence", "machine learning", "automation"],
        "skills": ["Python", "Machine Learning", "Data Analysis", "Problem Solving"],
        "description": "Build AI systems and intelligent applications.",
    },
    "Python Developer": {
        "keywords": ["python", "programming", "software", "development"],
        "skills": ["Python", "OOP", "Git and GitHub", "APIs"],
        "description": "Develop applications, scripts, and backend services.",
    },
    "Web Developer": {
        "keywords": ["web", "website", "frontend", "backend", "html", "css"],
        "skills": ["HTML", "CSS", "JavaScript", "Git and GitHub"],
        "description": "Create and maintain websites and web applications.",
    },
    "Data Analyst": {
        "keywords": ["data", "analytics", "statistics", "visualization"],
        "skills": ["Python", "SQL", "Excel", "Data Visualization"],
        "description": "Analyze data to discover useful patterns and insights.",
    },
    "Cybersecurity Analyst": {
        "keywords": ["cybersecurity", "security", "networks", "ethical hacking"],
        "skills": ["Networking", "Linux", "Security Fundamentals", "Python"],
        "description": "Help protect systems, networks, and information.",
    },
    "Java Developer": {
        "keywords": ["java", "object oriented", "oop", "software development"],
        "skills": ["Java", "OOP", "SQL", "Git and GitHub"],
        "description": "Build software applications using Java.",
    },
    "UI/UX Designer": {
        "keywords": ["design", "graphic design", "ui", "ux", "creative"],
        "skills": ["UI Design", "UX Research", "Prototyping", "Figma"],
        "description": "Design useful, accessible, and user-friendly digital products.",
    },
}


def recommend_careers(interests, skills, career_goal=""):
    """
    Return career recommendations as a list of dictionaries.
    Every result includes a reason field for app.py.
    """

    interests_text = " ".join(interests) if isinstance(interests, list) else str(interests or "")
    skills_text = " ".join(skills) if isinstance(skills, list) else str(skills or "")
    goal_text = str(career_goal or "")

    user_text = f"{interests_text} {skills_text} {goal_text}".lower()
    user_skills = {
        skill.strip().lower()
        for skill in (
            skills if isinstance(skills, list)
            else str(skills or "").replace(",", " ").split()
        )
        if skill.strip()
    }

    recommendations = []

    for career, details in CAREER_DATA.items():
        score = 0
        reasons = []

        # Match career interests and goals.
        matched_keywords = [
            keyword for keyword in details["keywords"]
            if keyword.lower() in user_text
        ]

        if matched_keywords:
            score += len(matched_keywords) * 2
            reasons.append(
                "Your interests or career goal relate to "
                + ", ".join(matched_keywords)
                + "."
            )

        # Match existing skills.
        matched_skills = [
            required_skill
            for required_skill in details["skills"]
            if any(
                required_skill.lower() == skill
                or required_skill.lower() in skill
                or skill in required_skill.lower()
                for skill in user_skills
            )
        ]

        if matched_skills:
            score += len(matched_skills) * 3
            reasons.append(
                "Your current skills match: "
                + ", ".join(matched_skills)
                + "."
            )

        # Give an additional score when the career goal names this career.
        if career.lower() in goal_text.lower():
            score += 10
            reasons.insert(0, "This career matches your stated career goal.")

        # Return relevant matches only.
        if score > 0:
            recommendations.append({
                "career": career,
                "title": career,
                "description": details["description"],
                "skills": details["skills"],
                "matched_skills": matched_skills,
                "score": score,
                "reason": " ".join(reasons) or (
                    "Recommended based on your interests and skills."
                ),
            })

    # Sort highest-scoring careers first.
    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Provide general suggestions if nothing matched.
    if not recommendations:
        recommendations = [
            {
                "career": "Python Developer",
                "title": "Python Developer",
                "description": CAREER_DATA["Python Developer"]["description"],
                "skills": CAREER_DATA["Python Developer"]["skills"],
                "matched_skills": [],
                "score": 0,
                "reason": (
                    "This is a general suggestion. Learn Python, "
                    "practice programming, and build small projects."
                ),
            },
            {
                "career": "AI Engineer",
                "title": "AI Engineer",
                "description": CAREER_DATA["AI Engineer"]["description"],
                "skills": CAREER_DATA["AI Engineer"]["skills"],
                "matched_skills": [],
                "score": 0,
                "reason": (
                    "This is a general suggestion. Start with Python "
                    "and gradually learn machine learning."
                ),
            },
        ]

    return recommendations
```
