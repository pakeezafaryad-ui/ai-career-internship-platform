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
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career & Internship Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

try:
    init_db()
except Exception as error:
    st.error("Could not initialize the database.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def split_items(text):
    """Convert comma-separated text into a list."""
    return [
        item.strip()
        for item in text.replace("\n", ",").split(",")
        if item.strip()
    ]


def display_result(result):
    """Display a result whether it is a dictionary, list, or text."""
    if isinstance(result, dict):
        for key, value in result.items():
            st.markdown(f"**{str(key).replace('_', ' ').title()}**")
            if isinstance(value, (dict, list)):
                st.json(value)
            else:
                st.write(value)

    elif isinstance(result, list):
        if not result:
            st.info("No results found.")
        else:
            for index, item in enumerate(result, start=1):
                with st.container(border=True):
                    st.markdown(f"**Result {index}**")
                    if isinstance(item, dict):
                        for key, value in item.items():
                            st.write(
                                f"{str(key).replace('_', ' ').title()}: "
                                f"{value}"
                            )
                    else:
                        st.write(item)
    else:
        st.write(result)


def safe_text(value, default="Not available"):
    """Return readable text for missing or empty values."""
    if value is None or value == "":
        return default
    return str(value)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎓 AI Career & Internship Platform")
st.caption(
    "Explore career paths, identify skill gaps, build learning roadmaps, "
    "find sample internships, and track your applications."
)

st.divider()


# --------------------------------------------------
# LOGIN AND REGISTRATION
# --------------------------------------------------

if st.session_state.user is None:

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            login_email = st.text_input(
                "Email",
                placeholder="you@example.com",
            )
            login_password = st.text_input(
                "Password",
                type="password",
            )
            login_submit = st.form_submit_button(
                "Login",
                type="primary",
                use_container_width=True,
            )

        if login_submit:
            email = login_email.strip().lower()

            if not email or not login_password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    user = authenticate_user(email, login_password)

                    if user:
                        st.session_state.user = user
                        st.session_state.page = "Dashboard"
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

                except Exception as error:
                    st.error("Login failed. Please try again.")
                    st.caption(str(error))

    with register_tab:
        st.subheader("Create your account")

        with st.form("register_form"):
            register_email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="register_email",
            )
            register_password = st.text_input(
                "Create password",
                type="password",
                key="register_password",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )
            register_submit = st.form_submit_button(
                "Create Account",
                type="primary",
                use_container_width=True,
            )

        if register_submit:
            email = register_email.strip().lower()

            if not email or "@" not in email:
                st.warning("Please enter a valid email address.")

            elif len(register_password) < 8:
                st.warning(
                    "Use a password with at least 8 characters."
                )

            elif register_password != confirm_password:
                st.error("The passwords do not match.")

            else:
                try:
                    success, message = register_user(
                        email,
                        register_password,
                    )

                    if success:
                        st.success(
                            "Account created successfully. "
                            "Please log in using the Login tab."
                        )
                    else:
                        st.error(str(message))

                except Exception as error:
                    st.error("Registration failed.")
                    st.caption(str(error))

    st.info(
        "Create an account or log in to access your personal dashboard. "
        "Use a test email and password while testing the project."
    )

    st.stop()


# --------------------------------------------------
# LOGGED-IN USER
# --------------------------------------------------

user = st.session_state.user
user_id = user["id"]
user_email = user.get("email", "User")


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.title("🧭 Navigation")
    st.write(f"Logged in as **{user_email}**")
    st.divider()

    pages = [
        "Dashboard",
        "Career Advisor",
        "Skill Gap Analyzer",
        "Learning Roadmap",
        "Job & Internship Matcher",
        "Application Tracker",
    ]

    selected_page = st.radio(
        "Choose a section",
        pages,
        index=(
            pages.index(st.session_state.page)
            if st.session_state.page in pages
            else 0
        ),
    )

    st.session_state.page = selected_page

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.rerun()

    st.caption("AI Career & Internship Platform")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if selected_page == "Dashboard":

    st.header("Your Career Dashboard")
    st.write(
        "Use the tools below to explore careers, develop skills, "
        "plan your learning, and organize internship applications."
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🧭 Career Advisor")
            st.write(
                "Get career suggestions based on your interests "
                "and current skills."
            )
            if st.button("Explore Careers", use_container_width=True):
                st.session_state.page = "Career Advisor"
                st.rerun()

        with st.container(border=True):
            st.subheader("📚 Learning Roadmap")
            st.write(
                "Create a step-by-step plan for your target career."
            )
            if st.button("Build Roadmap", use_container_width=True):
                st.session_state.page = "Learning Roadmap"
                st.rerun()

        with st.container(border=True):
            st.subheader("📋 Application Tracker")
            st.write(
                "Record and review the internships you have applied for."
            )
            if st.button("Track Applications", use_container_width=True):
                st.session_state.page = "Application Tracker"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("🎯 Skill Gap Analyzer")
            st.write(
                "Compare your current skills with the skills "
                "required for a career."
            )
            if st.button("Analyze Skills", use_container_width=True):
                st.session_state.page = "Skill Gap Analyzer"
                st.rerun()

        with st.container(border=True):
            st.subheader("💼 Job & Internship Matcher")
            st.write(
                "Explore sample opportunities and compare their "
                "requirements with your skills."
            )
            if st.button("Find Opportunities", use_container_width=True):
                st.session_state.page = "Job & Internship Matcher"
                st.rerun()

    st.divider()
    st.subheader("Project Information")
    st.write(
        "This version uses rule-based career recommendations and "
        "sample job listings. It does not fetch live vacancies."
    )


# --------------------------------------------------
# CAREER ADVISOR
# --------------------------------------------------

elif selected_page == "Career Advisor":

    st.header("🧭 AI Career Advisor")
    st.write(
        "Enter your interests and skills to receive career suggestions."
    )

    with st.form("career_form"):
        interests_text = st.text_area(
            "Your interests",
            placeholder="Artificial Intelligence, programming, automation",
        )

        career_skills_text = st.text_area(
            "Your current skills",
            placeholder="Python, Java, Git and GitHub",
        )

        career_goal = st.text_input(
            "Target career (optional)",
            placeholder="AI Engineer",
        )

        career_submit = st.form_submit_button(
            "Recommend Careers",
            type="primary",
        )

    if career_submit:
        interests = split_items(interests_text)
        skills = split_items(career_skills_text)

        if not interests and not skills and not career_goal.strip():
            st.warning(
                "Enter at least one interest, skill, or career goal."
            )
        else:
            try:
                recommendations = recommend_careers(
                    interests,
                    skills,
                    career_goal.strip(),
                )

                st.subheader("Your Career Recommendations")
                display_result(recommendations)

            except Exception as error:
                st.error("Could not generate career recommendations.")
                st.code(str(error))


# --------------------------------------------------
# SKILL GAP ANALYZER
# --------------------------------------------------

elif selected_page == "Skill Gap Analyzer":

    st.header("🎯 Skill Gap Analyzer")
    st.write(
        "Compare your current skills with a target career's "
        "expected skills."
    )

    with st.form("skill_gap_form"):
        current_skills_text = st.text_area(
            "Current skills",
            placeholder="Python, Pandas, SQL",
        )

        target_career = st.text_input(
            "Target career",
            placeholder="AI Engineer",
        )

        skill_gap_submit = st.form_submit_button(
            "Analyze Skill Gap",
            type="primary",
        )

    if skill_gap_submit:
        current_skills = split_items(current_skills_text)

        if not target_career.strip():
            st.warning("Please enter your target career.")
        else:
            try:
                result = analyze_skill_gap(
                    current_skills,
                    target_career.strip(),
                )

                st.subheader("Skill Gap Results")
                display_result(result)

            except Exception as error:
                st.error("Could not analyze the skill gap.")
                st.code(str(error))


# --------------------------------------------------
# LEARNING ROADMAP
# --------------------------------------------------

elif selected_page == "Learning Roadmap":

    st.header("📚 Learning Roadmap Generator")
    st.write(
        "Create a learning plan based on your target career, "
        "existing skills, and available time."
    )

    with st.form("roadmap_form"):
        roadmap_career = st.text_input(
            "Target career",
            placeholder="Python Developer",
        )

        roadmap_skills_text = st.text_area(
            "Current skills",
            placeholder="Python, Java, Git and GitHub",
        )

        weeks = st.selectbox(
            "Roadmap duration",
            [4, 6, 8, 10, 12, 16, 24],
            index=2,
            format_func=lambda value: f"{value} weeks",
        )

        roadmap_submit = st.form_submit_button(
            "Generate Roadmap",
            type="primary",
        )

    if roadmap_submit:
        if not roadmap_career.strip():
            st.warning("Please enter a target career.")
        else:
            try:
                current_skills = split_items(roadmap_skills_text)

                roadmap = generate_learning_roadmap(
                    roadmap_career.strip(),
                    current_skills,
                    weeks,
                )

                st.subheader("Your Learning Roadmap")

                if isinstance(roadmap, dict):
                    title = roadmap.get("title", roadmap_career)
                    st.markdown(f"### {title}")

                    plan = roadmap.get(
                        "plan",
                        roadmap.get(
                            "weeks",
                            roadmap.get("roadmap", []),
                        ),
                    )

                    if isinstance(plan, list):
                        for index, step in enumerate(plan, start=1):
                            with st.container(border=True):
                                if isinstance(step, dict):
                                    heading = (
                                        step.get("week")
                                        or step.get("title")
                                        or step.get("topic")
                                        or f"Step {index}"
                                    )
                                    st.markdown(f"**{heading}**")

                                    details = (
                                        step.get("tasks")
                                        or step.get("activities")
                                        or step.get("description")
                                        or step.get("content")
                                    )

                                    if isinstance(details, list):
                                        for detail in details:
                                            st.write(f"- {detail}")
                                    elif details:
                                        st.write(details)
                                    else:
                                        st.json(step)
                                else:
                                    st.markdown(
                                        f"**Step {index}:** {step}"
                                    )

                    elif isinstance(plan, str):
                        st.write(plan)
                    else:
                        display_result(plan)

                elif isinstance(roadmap, list):
                    for index, step in enumerate(roadmap, start=1):
                        st.markdown(f"**Step {index}**")
                        display_result(step)

                else:
                    st.write(roadmap)

                if st.button(
                    "💾 Save This Roadmap",
                    type="primary",
                    key="save_roadmap_button",
                ):
                    try:
                        saved = save_roadmap(user_id, roadmap)

                        if saved:
                            st.success(
                                "Roadmap saved to your account."
                            )
                        else:
                            st.warning(
                                "The save function did not confirm "
                                "success. Check services/learning_roadmap.py."
                            )
                    except Exception as error:
                        st.error("Could not save the roadmap.")
                        st.code(str(error))

            except Exception as error:
                st.error("Could not generate the learning roadmap.")
                st.code(str(error))

    st.divider()
    st.subheader("Previously Saved Roadmaps")

    try:
        saved_roadmaps = get_user_roadmaps(user_id) or []

        if not saved_roadmaps:
            st.info("Your saved roadmaps will appear here.")
        else:
            for item in saved_roadmaps:
                with st.container(border=True):
                    if isinstance(item, dict):
                        title = item.get("title", "Learning Roadmap")
                        st.markdown(f"**{title}**")

                        plan = item.get("plan")
                        if plan is not None:
                            display_result(plan)

                        progress = item.get("progress_percent", 0)
                        try:
                            progress = max(
                                0,
                                min(100, int(float(progress))),
                            )
                            st.progress(
                                progress,
                                text=f"Progress: {progress}%",
                            )
                        except (TypeError, ValueError):
                            pass
                    else:
                        display_result(item)

    except Exception as error:
        st.warning("Could not load saved roadmaps.")
        st.caption(str(error))


# --------------------------------------------------
# JOB AND INTERNSHIP MATCHER
# --------------------------------------------------

elif selected_page == "Job & Internship Matcher":

    st.header("💼 Job & Internship Matcher")
    st.write(
        "Enter your skills to compare them with the project's "
        "sample opportunities."
    )

    with st.form("job_match_form"):
        job_skills_text = st.text_area(
            "Your skills",
            placeholder="Python, SQL, Git and
