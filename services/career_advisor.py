def recommend_careers(interests, skills, career_goal=""):
    """Recommend careers using the user's interests and skills."""

    career_data = [
        {
            "career": "AI Engineer",
            "description": "Build AI applications, chatbots, and intelligent systems.",
            "skills": ["python", "machine learning", "ai", "data science"],
            "interests": ["artificial intelligence", "ai", "automation", "machine learning"],
            "learning": "Learn Python, NumPy, Pandas, machine learning, and APIs."
        },
        {
            "career": "Python Developer",
            "description": "Develop applications and automate everyday tasks using Python.",
            "skills": ["python", "sql", "api", "git"],
            "interests": ["programming", "software", "automation", "coding"],
            "learning": "Practice Python, functions, OOP, SQL, APIs, and GitHub."
        },
        {
            "career": "Web Developer",
            "description": "Create and maintain websites and web applications.",
            "skills": ["html", "css", "javascript", "python"],
            "interests": ["web development", "websites", "design", "programming"],
            "learning": "Learn HTML, CSS, JavaScript, responsive design, and Git."
        },
        {
            "career": "Cybersecurity Analyst",
            "description": "Help organizations protect systems and information.",
            "skills": ["networking", "linux", "python", "security"],
            "interests": ["cybersecurity", "security", "networks", "ethical hacking"],
            "learning": "Study networking, Linux, security fundamentals, and safe labs."
        },
        {
            "career": "Data Analyst",
            "description": "Use data to discover patterns and support decisions.",
            "skills": ["python", "sql", "excel", "pandas", "statistics"],
            "interests": ["data", "statistics", "analysis", "business"],
            "learning": "Learn Excel, SQL, Python, Pandas, and data visualization."
        },
        {
            "career": "Java Developer",
            "description": "Build software applications using Java.",
            "skills": ["java", "oop", "sql", "git"],
            "interests": ["java", "software development", "programming", "coding"],
            "learning": "Practice Java, OOP, collections, databases, and projects."
        }
    ]

    user_skills = [
        item.strip().lower()
        for item in (skills or "").replace(",", "\n").splitlines()
        if item.strip()
    ]

    user_interests = [
        item.strip().lower()
        for item in (interests or "").replace(",", "\n").splitlines()
        if item.strip()
    ]

    goal = (career_goal or "").strip().lower()
    results = []

    for item in career_data:
        matching_skills = [
            skill for skill in item["skills"]
            if any(skill in user_skill or user_skill in skill
                   for user_skill in user_skills)
        ]

        matching_interests = [
            interest for interest in item["interests"]
            if any(interest in user_interest or user_interest in interest
                   for user_interest in user_interests)
        ]

        goal_match = bool(
            goal and (
                goal in item["career"].lower()
                or item["career"].lower() in goal
            )
        )

        score = (
            len(matching_skills) * 2
            + len(matching_interests)
            + (4 if goal_match else 0)
        )

        if score > 0:
            results.append({
                "career": item["career"],
                "description": item["description"],
                "matching_skills": matching_skills,
                "reason": (
                    f"Matches {len(matching_skills)} of this career's listed "
                    f"skills and {len(matching_interests)} related interests."
                ),
                "learning": item["learning"],
                "score": score
            })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:5]
