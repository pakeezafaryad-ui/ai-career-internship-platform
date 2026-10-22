import streamlit as st

from services.database import init_db
from services.auth_service import register_user, authenticate_user
from services.career_advisor import recommend_careers
from services.skill_gap import analyze_skill_gap
from services.learning_roadmap import (
    generate_learning_roadmap,
    save_roadmap,
    get_user_roadmaps,
)
from services.job_matcher import match_jobs
from services.application_tracker import (
    add_application,
    get_user_applications,
    update_application_status,
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SIMPLE, MODERN DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7f8ff 0%, #eef5ff 100%);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }

    .hero {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(120deg, #3730a3, #6366f1, #0ea5e9);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 2.3rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: white;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.9);
        border-radius: 16px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    h1, h2, h3 {
        color: #25245c;
    }

    .small-note {
        color: #5b6475;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DATABASE AND SESSION STATE
# --------------------------------------------------

init_db()

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def safe_text(value, default="Not available"):
    """Convert a value to readable text safely."""
    if value is None or value == "":
        return default

    if isinstance(value, list):
        return ", ".join(str(x) for x in value) if value else default

    return str(value)


def show_hero():
    st.markdown(
        """
        <div class="hero">
            <h1>🎓 CareerPath AI</h1>
            <p>
                Discover career paths, identify skill gaps, create a learning
                roadmap, and organize your internship applications.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_login():
    st.title("Welcome to CareerPath AI")
    st.write("Create an account or sign in to access your career dashboard.")

    login_tab, register_tab = st.tabs(["🔐 Sign In", "✨ Create Account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email address", key="login_email")
            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )
            submitted = st.form_submit_button(
                "Sign In",
                use_container_width=True,
            )

        if submitted:
            email = email.strip().lower()

            if not email or not password:
                st.warning("Please enter both your email and password.")
            else:
                try:
                    user = authenticate_user(email, password)

                    if user:
                        st.session_state.user = user
                        st.session_state.page = "Home"
                        st.rerun()
                    else:
                        st.error("Incorrect email or password.")
                except Exception:
                    st.error(
                        "We could not sign you in. Please check the app logs "
                        "if the problem continues."
                    )

    with register_tab:
        with st.form("register_form"):
            new_email = st.text_input("Email address", key="register_email")
            new_password = st.text_input(
                "Create password",
                type="password",
                key="register_password",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )
            create = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if create:
            new_email = new_email.strip().lower()

            if not new_email or not new_password:
                st.warning("Please fill in all fields.")
            elif "@" not in new_email or "." not in new_email.split("@")[-1]:
                st.warning("Please enter a valid email address.")
            elif len(new_password) < 8:
                st.warning("Use a password with at least 8 characters.")
            elif new_password != confirm_password:
                st.warning("The passwords do not match.")
            else:
                try:
                    success, message = register_user(
                        new_email,
                        new_password,
                    )

                    if success:
                        st.success(
                            "Account created! You can now sign in."
                        )
                    else:
                        st.error(message)
                except Exception:
                    st.error(
                        "We could not create the account. Please try again."
                    )


# --------------------------------------------------
# CAREER ADVISOR
# --------------------------------------------------

def career_advisor_page():
    st.header("🧭 Find Suitable Career Paths")
    st.write(
        "Tell us what you enjoy and which skills you have. "
        "We'll suggest career paths to explore."
    )

    with st.form("career_advisor_form"):
        interests = st.text_area(
            "Your interests",
            placeholder="Example: Artificial Intelligence, programming, automation",
        )

        skills = st.text_area(
            "Your current skills",
            placeholder="Example: Python, Java, Git and GitHub",
        )

        career_goal = st.text_input(
            "Career goal (optional)",
            placeholder="Example: AI Engineer",
        )

        submitted = st.form_submit_button(
            "Find My Career Paths ✨",
            use_container_width=True,
        )

    if submitted:
        if not interests.strip() and not skills.strip() and not career_goal.strip():
            st.warning("Enter at least an interest, a skill, or a career goal.")
            return

        try:
            recommendations = recommend_careers(
                interests=interests,
                skills=skills,
                career_goal=career_goal,
            )

            if not recommendations:
                st.info(
                    "No close matches found. Try adding broader interests "
                    "or more skills."
                )
                return

            st.subheader("Your Career Suggestions")
            st.caption(
                "These are rule-based suggestions, not a guarantee of "
                "career suitability."
            )

            for item in recommendations:
                career = item.get("career", "Career option")
                description = item.get(
                    "description",
                    "Explore this career to learn more.",
                )
                reason = item.get(
                    "reason",
                    "This career may relate to your interests or skills.",
                )
                matching_skills = item.get(
                    "matching_skills",
                    item.get("matched_skills", []),
                )
                learning = item.get(
                    "learning",
                    "Explore beginner courses and build a small project.",
                )

                with st.container(border=True):
                    st.markdown(f"### 🎯 {career}")
                    st.write(description)

                    st.markdown("**Why consider this career?**")
                    st.write(reason)

                    if matching_skills:
                        st.markdown("**Skills you already have**")
                        st.write(safe_text(matching_skills))

                    st.markdown("**Recommended next step**")
                    st.write(learning)

                    if st.button(
                        "Use this career for my skill-gap analysis",
                        key=f"career_{career}",
                    ):
                        st.session_state.selected_career = career
                        st.session_state.page = "Skill Gap Analyzer"
                        st.rerun()

        except Exception as error:
            st.error("Career recommendations could not be generated.")
            st.caption(f"Details: {error}")


# --------------------------------------------------
# SKILL GAP ANALYZER
# --------------------------------------------------

def skill_gap_page():
    st.header("🧩 Skill Gap Analyzer")
    st.write(
        "Compare your current skills with the skills needed for your "
        "target career."
    )

    selected_career = st.session_state.get("selected_career", "")

    with st.form("skill_gap_form"):
        target_career = st.text_input(
            "Target career",
            value=selected_career,
            placeholder="Example: AI Engineer",
        )

        current_skills = st.text_area(
            "Skills you already have",
            placeholder="Example: Python, Pandas, Java",
        )

        submitted = st.form_submit_button(
            "Analyze My Skills",
            use_container_width=True,
        )

    if submitted:
        if not target_career.strip():
            st.warning("Please enter your target career.")
            return

        try:
            result = analyze_skill_gap(
                current_skills,
                target_career.strip(),
            )

            if isinstance(result, dict):
                matched = result.get(
                    "matched_skills",
                    result.get("matching_skills", []),
                )
                missing = result.get(
                    "missing_skills",
                    result.get("skills_to_learn", []),
                )
                percentage = result.get(
                    "match_percentage",
                    result.get("match_percent", result.get("match_score")),
                )

                st.subheader(f"Your Skill Gap: {target_career}")

                if isinstance(percentage, (int, float)):
                    percentage = max(0, min(100, percentage))
                    st.metric("Current Skill Match", f"{percentage:.0f}%")
                    st.progress(percentage / 100)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### ✅ Skills you have")
                    if matched:
                        for skill in matched:
                            st.write(f"• {skill}")
                    else:
                        st.info("No matching skills identified yet.")

                with col2:
                    st.markdown("#### 📚 Skills to learn")
                    if missing:
                        for skill in missing:
                            st.write(f"• {skill}")
                    else:
                        st.success("No missing skills were returned.")

                st.info(
                    "Use this result as a learning guide. Skill matching "
                    "depends on the rules configured in this project."
                )
            else:
                st.write(result)

        except Exception as error:
            st.error("Skill-gap analysis could not be completed.")
            st.caption(f"Details: {error}")


# --------------------------------------------------
# LEARNING ROADMAP
# --------------------------------------------------

def roadmap_page():
    st.header("🗺️ Your Learning Roadmap")
    st.write(
        "Create a step-by-step plan to work toward your target career."
    )

    with st.form("roadmap_form"):
        target_career = st.text_input(
            "Career you want to pursue",
            placeholder="Example: Python Developer",
        )

        current_skills = st.text_area(
            "Skills you already know",
            placeholder="Example: Python, Java",
        )

        duration = st.selectbox(
            "How many weeks do you want your plan to cover?",
            [4, 6, 8, 12, 16],
            index=2,
        )

        submitted = st.form_submit_button(
            "Generate My Roadmap",
            use_container_width=True,
        )

    if submitted:
        if not target_career.strip():
            st.warning("Please enter a target career.")
            return

        try:
            roadmap = generate_learning_roadmap(
                target_career.strip(),
                current_skills=current_skills,
                duration_weeks=duration,
            )

            st.session_state.generated_roadmap = roadmap
            st.session_state.roadmap_career = target_career.strip()
            st.session_state.roadmap_duration = duration

        except Exception as error:
            st.error("We could not generate your roadmap.")
            st.caption(f"Details: {error}")

    if "generated_roadmap" in st.session_state:
        roadmap = st.session_state.generated_roadmap

        st.subheader(
            f"Learning Plan: {st.session_state.get('roadmap_career', 'Your career')}"
        )

        if isinstance(roadmap, dict):
            for key, value in roadmap.items():
                st.markdown(f"**{str(key).replace('_', ' ').title()}**")
                if isinstance(value, list):
                    for entry in value:
                        st.write(f"• {entry}")
                else:
                    st.write(safe_text(value))
        elif isinstance(roadmap, list):
            for index, entry in enumerate(roadmap, start=1):
                with st.container(border=True):
                    if isinstance(entry, dict):
                        st.markdown(
                            f"### Week {entry.get('week', index)}"
                        )
                        for key, value in entry.items():
                            if key != "week":
                                st.write(
                                    f"**{str(key).replace('_', ' ').title()}:** "
                                    f"{safe_text(value)}"
                                )
                    else:
                        st.markdown(f"### Step {index}")
                        st.write(entry)
        else:
            st.write(roadmap)

        if st.button("Save Roadmap to My Account"):
            try:
                success = save_roadmap(
                    st.session_state.user["id"],
                    roadmap,
                )

                if success:
                    st.success("Your roadmap has been saved.")
                else:
                    st.error("The roadmap could not be saved.")
            except Exception as error:
                st.error("Could not save the roadmap.")
                st.caption(f"Details: {error}")


# --------------------------------------------------
# JOB AND INTERNSHIP MATCHER
# --------------------------------------------------

def jobs_page():
    st.header("💼 Find Matching Jobs & Internships")
    st.write(
        "Enter your skills to explore example job listings from the "
        "project's sample dataset."
    )

    with st.form("jobs_form"):
        skills = st.text_area(
            "Your skills",
            placeholder="Example: Python, SQL, Git, REST APIs",
        )

        target_role = st.text_input(
            "Preferred role (optional)",
            placeholder="Example: Python Developer Intern",
        )

        submitted = st.form_submit_button(
            "Find Matching Opportunities",
            use_container_width=True,
        )

    if submitted:
        if not skills.strip():
            st.warning("Enter at least one skill.")
            return

        try:
            jobs = match_jobs(
                skills,
                target_role=target_role.strip() or None,
            )

            if not jobs:
                st.info(
                    "No matching sample listings were found. Try adding "
                    "more skills or changing your preferred role."
                )
                return

            st.subheader("Matching Opportunities")
            st.caption(
                "These may be sample listings, not live vacancies. "
                "Check the employer's official website before applying."
            )

            for job in jobs:
                title = job.get("title", "Untitled role")
                company = job.get("company", "Company not specified")
                description = job.get(
                    "description",
                    "No description provided.",
                )
                match_percent = job.get(
                    "match_percent",
                    job.get("match_percentage"),
                )
                matched = job.get("matched_skills", [])
                missing = job.get("missing_skills", [])
                source_type = job.get("source_type", "sample")
                application_url = job.get("application_url", "")

                with st.container(border=True):
                    st.markdown(f"### 💼 {title}")
                    st.markdown(f"**Company:** {company}")

                    if isinstance(match_percent, (int, float)):
                        st.metric("Skill Match", f"{match_percent:.0f}%")

                    st.write(description)

                    if matched:
                        st.markdown("**Skills that match**")
                        st.write(safe_text(matched))

                    if missing:
                        st.markdown("**Skills to improve**")
                        st.write(safe_text(missing))

                    st.caption(f"Listing source: {source_type}")

                    if application_url:
                        st.link_button(
                            "View application page",
                            application_url,
                        )
                    else:
                        st.caption(
                            "No application link is available for this "
                            "sample listing."
                        )

        except Exception as error:
            st.error("Job matching could not be completed.")
            st.caption(f"Details: {error}")


# --------------------------------------------------
# APPLICATION TRACKER
# --------------------------------------------------

def applications_page():
    st.header("📌 Internship Application Tracker")
    st.write(
        "Keep a record of opportunities you have applied for."
    )

    with st.form("add_application_form"):
        company = st.text_input(
            "Company name",
            placeholder="Example: DemoTech Solutions",
        )

        role = st.text_input(
            "Job or in
