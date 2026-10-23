
def recommend_careers(interests, skills, career_goal=""):
    """Recommend career paths using simple rule-based matching."""

    # Accept either text or lists so both formats work.
    def normalize(value):
        if isinstance(value, str):
            return [
                item.strip().lower()
                for item in value.replace("\n", ",").split(",")
                if item.strip()
            ]

        if isinstance(value, (list, tuple, set)):
            return [
                str(item).strip().lower()
                for item in value
                if str(item).strip()
            ]

        if value is None:
            return []

        return [str(value).strip().lower()]

    interests_list = normalize(interests)
    skills_list = normalize(skills)
    goal = str(career_goal or "").strip().lower()

    all_inputs = interests_list + skills_list + ([goal] if goal else [])

    careers = {
        "AI Engineer": [
            "artificial intelligence", "ai", "machine learning",
            "python", "automation", "data science"
        ],
        "Software Developer": [
            "programming", "software", "java", "python",
            "coding", "development"
        ],
        "Web Developer": [
            "web", "html", "css", "javascript", "website",
            "frontend", "backend"
        ],
        "Data Analyst": [
            "data", "statistics", "excel", "sql", "pandas",
            "visualization", "analytics"
        ],
        "Cybersecurity Analyst": [
            "cybersecurity", "security", "network", "ethical hacking",
            "linux", "privacy"
        ],
        "Cloud Engineer": [
            "cloud", "aws", "azure", "deployment", "devops",
            "servers"
        ],
        "Mobile App Developer": [
            "mobile", "android", "ios", "app development",
            "flutter", "kotlin"
        ],
        "UI/UX Designer": [
            "design", "ui", "ux", "figma", "creative",
            "user experience"
        ],
    }

    results = []

    for career, keywords in careers.items():
        score = sum(
            1 for item in all_inputs
            if any(keyword in item for keyword in keywords)
        )

        if goal and (
            goal in career.lower() or career.lower() in goal
        ):
            score += 5

        if score > 0:
            results.append({
                "career": career,
                "match_score": score,
                "reason": (
                    f"This career may suit you because some of your "
                    f"interests or skills relate to {career.lower()}."
                ),
                "suggested_next_step": (
                    f"Learn the basic tools and complete a small "
                    f"{career.lower()} project."
                ),
            })

    results.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    if not results:
        results = [{
            "career": "Software Developer",
            "match_score": 1,
            "reason": (
                "Software development is a broad starting point "
                "for students interested in technology."
            ),
            "suggested_next_step": (
                "Build a small programming project and explore "
                "different technology careers."
            ),
        }]

    return results[:5]
