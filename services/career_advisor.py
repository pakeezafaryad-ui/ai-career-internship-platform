def recommend_careers(interests, skills, career_goal=""):
    """
    Recommend career paths based on a user's interests,
    existing skills, and career goals.
    """

    career_profiles = {
        "AI Engineer": {
            "interests": [
                "artificial intelligence", "ai", "machine learning",
                "automation", "research", "data"
            ],
            "skills": [
                "python", "machine learning", "statistics",
                "data analysis", "numpy", "pandas", "apis"
            ],
            "description": (
                "Build AI-powered applications and machine learning solutions."
            ),
            "learning_focus": [
                "Python", "Machine Learning", "Data Analysis", "AI APIs"
            ],
        },
        "Python Developer": {
            "interests": [
                "programming", "software development",
                "automation", "backend", "coding"
            ],
            "skills": [
                "python", "programming", "git and github", "sql", "rest apis"
            ],
            "description": (
                "Develop applications, automation scripts, and backend services."
            ),
            "learning_focus": [
                "Python Fundamentals", "Object-Oriented Programming",
                "APIs", "Databases"
            ],
        },
        "Data Analyst": {
            "interests": [
                "data", "statistics", "business",
                "research", "visualization", "reports"
            ],
            "skills": [
                "excel", "sql", "python", "statistics",
                "pandas", "data visualization"
            ],
            "description": (
                "Analyze data and prepare reports to support decisions."
            ),
            "learning_focus": [
                "Excel", "SQL", "Statistics", "Data Visualization"
            ],
        },
        "Web Developer": {
            "interests": [
                "websites", "web development", "frontend",
                "design", "backend", "coding"
            ],
            "skills": [
                "html", "css", "javascript", "python", "sql", "rest apis"
            ],
            "description": (
                "Create and maintain websites and web applications."
            ),
            "learning_focus": [
                "HTML and CSS", "JavaScript",
                "Web Frameworks", "Databases"
            ],
        },
        "Java Developer": {
            "interests": [
                "java", "programming", "software development",
                "applications", "object oriented programming"
            ],
            "skills": [
                "java", "object-oriented programming",
                "data structures", "sql", "git and github"
            ],
            "description": (
                "Build software applications using Java and OOP principles."
            ),
            "learning_focus": [
                "Java", "Object-Oriented Programming",
                "Data Structures", "Databases"
            ],
        },
        "Cybersecurity Analyst": {
            "interests": [
                "cybersecurity", "security", "networks",
                "privacy", "ethical hacking", "risk"
            ],
            "skills": [
                "networking", "linux", "python",
                "security fundamentals", "risk assessment"
            ],
            "description": (
                "Help protect systems and data by identifying security risks."
            ),
            "learning_focus": [
                "Networking", "Linux",
                "Security Fundamentals", "Risk Management"
            ],
        },
        "Machine Learning Engineer": {
            "interests": [
                "machine learning", "artificial intelligence",
                "data", "mathematics", "model training", "research"
            ],
            "skills": [
                "python", "statistics", "linear algebra",
                "machine learning", "data processing", "model evaluation"
            ],
            "description": (
                "Develop and evaluate machine learning models."
            ),
            "learning_focus": [
                "Python", "Statistics", "Machine Learning",
                "Model Evaluation"
            ],
        },
        "Full Stack Developer": {
            "interests": [
                "web development", "websites", "frontend",
                "backend", "software development"
            ],
            "skills": [
                "html", "css", "javascript",
                "python", "sql", "rest apis"
            ],
            "description": (
                "Build both frontend interfaces and backend systems."
            ),
            "learning_focus": [
                "HTML and CSS", "JavaScript",
                "Backend Development", "Databases"
            ],
        },
    }

    # Convert inputs into lists of strings.
    def normalize_input(value):
        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        if isinstance(value, (list, tuple, set)):
            return [
                item.strip()
                for item in value
                if isinstance(item, str) and item.strip()
            ]

        return []

    user_interests = [
        item.casefold() for item in normalize_input(interests)
    ]
    user_skills = [
        item.casefold() for item in normalize_input(skills)
    ]
    user_goals = [
        item.casefold() for item in normalize_input(career_goal)
    ]

    recommendations = []

    for career, profile in career_profiles.items():
        interest_matches = sum(
            1
            for interest in user_interests
            if any(
                interest in category or category in interest
                for category in profile["interests"]
            )
        )

        skill_matches = sum(
            1
            for skill in user_skills
            if skill in profile["skills"]
        )

        goal_matches = sum(
            1
            for goal in user_goals
            if any(
                goal in category or category in goal
                for category in profile["interests"]
            )
        )

        score = (
            interest_matches * 3
            + skill_matches * 2
            + goal_matches * 4
        )

        recommendations.append({
            "career": career,
            "score": score,
            "description": profile["description"],
            "matched_skills": [
                skill
                for skill in normalize_input(skills)
                if skill.casefold() in profile["skills"]
            ],
            "learning_focus": profile["learning_focus"],
        })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return recommendations[:5]
