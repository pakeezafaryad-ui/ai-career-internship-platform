import streamlit as st
import json
from pathlib import Path

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
    page_title="CareerPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# INTERFACE DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f6f8fc;
    }

    [data-testid="stSidebar"] {
        background-color: #172554;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #4f46e5);
        color: white;
        margin-bottom: 20px;
    }

    .hero h1, .hero p {
        color: white;
    }

    div.stButton > button[kind="primary"] {
        background-color: #4f46e5 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* Make the sidebar Log out button visible */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: 1px solid #60A5FA !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

try:
    init_db()
except Exception as error:
    st.error("The database could not be initialized.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def split_items(text):
    """Convert comma-separated skills or interests into a list."""
    return [
        item.strip()
        for item in text.replace("\n", ",").split(",")
        if item.strip()
    ]


def show_result(value):
    """Display results whether they are dictionaries, lists, or text."""
    if isinstance(value, (dict, list)):
        st.json(value)
    else:
        st.write(value)


def get_field(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def show_error(message, error):
    st.error(message)
    with st.expander("Technical details"):
        st.code(str(error))


def require_login():
    return st.session_state.get("user") is not None


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# --------------------------------------------------
# LOGIN AND REGISTRATION
# --------------------------------------------------

if not require_login():
    st.markdown(
        """
        <div class="hero">
            <h1>🎓 CareerPath AI</h1>
            <p>Your simple guide to careers, skills, learning and internships.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    with login_tab:
        st.subheader("Welcome back")
        st.write("Log in to continue your career journey.")

        with st.form("login_form"):
            login_email = st.text_input("Email address")
            login_password = st.text_input(
                "Password", type="password"
            )
            login_submit = st.form_submit_button(
                "Login", type="primary", use_container_width=True
            )

        if login_submit:
            if not login_email.strip() or not login_password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    user = authenticate_user(
                        login_email.strip().lower(),
                        login_password,
                    )
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Login failed. Check your details.")
                except Exception as error:
                    show_error("Could not log you in.", error)

    with register_tab:
        st.subheader("Create your account")
        st.write("Create an account to save your learning progress.")

        with st.form("register_form"):
            new_email = st.text_input("Email address", key="reg_email")
            new_password = st.text_input(
                "Create password",
                type="password",
                key="reg_password",
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
            if not new_email.strip() or not new_password:
                st.warning("Please complete all fields.")
            elif new_password != confirm_password:
                st.error("The passwords do not match.")
            elif len(new_password) < 8:
                st.warning("Use a password with at least 8 characters.")
            else:
                try:
                    result = register_user(
                        new_email.strip().lower(),
                        new_password,
                    )
                    success, message = result
                    if success:
                        st.success(
                            "Account created! Open the Login tab to sign in."
                        )
                    else:
                        st.error(message)
                except Exception as error:
                    show_error("Could not create the account.", error)

    st.stop()


# --------------------------------------------------
# LOGGED-IN USER
# --------------------------------------------------

user = st.session_state.user
user_id = get_field(user, "id")
user_email = get_field(user, "email", "User")

st.sidebar.title("🎓 CareerPath AI")
st.sidebar.caption("Your personal career assistant")
st.sidebar.divider()
st.sidebar.write(f"👤 {user_email}")

pages = [
    "Dashboard",
    "Career Advisor",
    "Skill Gap Analyzer",
    "Learning Roadmap",
    "Job & Internship Matcher",
    "Application Tracker",
]

selected_page = st.sidebar.radio(
    "Navigate",
    pages,
    index=pages.index(st.session_state.page)
    if st.session_state.page in pages else 0,
)

st.session_state.page = selected_page

if st.sidebar.button("Log out", use_container_width=True):
    st.session_state.user = None
    st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if selected_page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to CareerPath AI! 👋</h1>
            <p>
                Discover careers, identify missing skills, build a learning
                plan, and organize your internship applications.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Your career toolkit")

    cards = [
        ("🧭 Career Advisor", "Explore careers that fit your interests."),
        ("🎯 Skill Gap Analyzer", "Find skills you need to develop."),
        ("📚 Learning Roadmap", "Create a step-by-step study plan."),
        ("💼 Job Matcher", "Compare your skills with sample opportunities."),
        ("📋 Application Tracker", "Keep track of your applications."),
    ]

    columns = st.columns(3)
    for index, (title, description) in enumerate(cards):
        with columns[index % 3]:
            with st.container(border=True):
                st.subheader(title)
                st.write(description)

    st.info(
        "Start with Career Advisor, then use Skill Gap Analyzer "
        "to decide what to learn next."
    )

    st.caption(
        "Note: Sample job listings are demonstration data, not verified "
        "live vacancies."
    )


# --------------------------------------------------
# CAREER ADVISOR
# --------------------------------------------------

elif selected_page == "Career Advisor":
    st.title("🧭 Career Advisor")
    st.write(
        "Tell us what you enjoy and what you know. "
        "We'll suggest career paths to explore."
    )

    with st.form("career_form"):
        interests_text = st.text_area(
            "Your interests",
            placeholder="Artificial Intelligence, programming, automation",
        )
        skills_text = st.text_area(
            "Your current skills",
            placeholder="Python, Java, Git and GitHub",
        )
        career_goal = st.text_input(
            "Your career goal (optional)",
            placeholder="AI Engineer",
        )
        submit = st.form_submit_button(
            "Recommend Careers", type="primary"
        )

    if submit:
        interests = split_items(interests_text)
        skills = split_items(skills_text)

        if not interests and not skills and not career_goal.strip():
            st.warning("Enter at least an interest, a skill, or a career goal.")
        else:
            try:
                results = recommend_careers(
                    interests,
                    skills,
                    career_goal.strip(),
                )
                st.subheader("Your career suggestions")
                show_result(results)
            except Exception as error:
                show_error("Could not generate career suggestions.", error)


# --------------------------------------------------
# SKILL GAP ANALYZER
# --------------------------------------------------

elif selected_page == "Skill Gap Analyzer":
    st.title("🎯 Skill Gap Analyzer")
    st.write(
        "Compare your current skills with the skills commonly needed "
        "for your target career."
    )

    with st.form("skill_gap_form"):
        skills_text = st.text_area(
            "Skills you already have",
            placeholder="Python, Java, SQL",
        )
        target_career = st.text_input(
            "Target career",
            placeholder="AI Engineer",
        )
        submit = st.form_submit_button(
            "Analyze My Skills", type="primary"
        )

    if submit:
        skills = split_items(skills_text)

        if not target_career.strip():
            st.warning("Please enter a target career.")
        else:
            try:
                result = analyze_skill_gap(
                    skills,
                    target_career.strip(),
                )
                st.subheader("Your skill analysis")
                show_result(result)
            except Exception as error:
                show_error("Could not analyze your skills.", error)


# --------------------------------------------------
# LEARNING ROADMAP
# --------------------------------------------------

elif selected_page == "Learning Roadmap":
    st.title("📚 Learning Roadmap")
    st.write(
        "Create a learning plan that breaks your career goal into "
        "smaller, manageable steps."
    )

    with st.form("roadmap_form"):
        roadmap_career = st.text_input(
            "Career you want to prepare for",
            placeholder="Python Developer",
        )
        roadmap_skills_text = st.text_area(
            "Skills you already know",
            placeholder="Python, Java",
        )
        weeks = st.select_slider(
            "How many weeks do you want to plan for?",
            options=[2, 4, 6, 8, 12, 16, 24],
            value=8,
        )
        roadmap_submit = st.form_submit_button(
            "Generate Roadmap", type="primary"
        )

    if roadmap_submit:
        if not roadmap_career.strip():
            st.warning("Please enter your target career.")
        else:
            try:
                current_skills = split_items(roadmap_skills_text)
                roadmap = generate_learning_roadmap(
                    roadmap_career.strip(),
                    current_skills,
                    weeks,
                )

                st.subheader("Your learning plan")
                show_result(roadmap)

                if st.button("Save This Roadmap", type="primary"):
                    saved = save_roadmap(user_id, roadmap)
                    if saved:
                        st.success("Your roadmap was saved.")
                    else:
                        st.warning(
                            "The save function did not confirm success. "
                            "Check services/learning_roadmap.py."
                        )
            except Exception as error:
                show_error("Could not create the learning roadmap.", error)

    st.divider()
    st.subheader("Previously saved roadmaps")

    try:
        saved_roadmaps = get_user_roadmaps(user_id) or []
        if not saved_roadmaps:
            st.info("Your saved roadmaps will appear here.")
        else:
            for index, item in enumerate(saved_roadmaps):
                with st.expander(
                    str(get_field(item, "title", "Learning roadmap"))
                ):
                    show_result(
                        get_field(item, "plan", item)
                    )
    except Exception as error:
        show_error("Could not load saved roadmaps.", error)


# --------------------------------------------------
# JOB AND INTERNSHIP MATCHER
# --------------------------------------------------

elif selected_page == "Job & Internship Matcher":
    st.title("💼 Job & Internship Matcher")
    st.write(
        "Enter your skills to compare them with the project's sample "
        "opportunities. These are not live job listings."
    )

    with st.form("job_match_form"):
        job_skills_text = st.text_area(
            "Your skills",
            placeholder="Python, SQL, Git and GitHub, REST APIs",
        )
        target_role = st.text_input(
            "Preferred role (optional)",
            placeholder="Python Developer Intern",
        )
        job_submit = st.form_submit_button(
            "Find Matches", type="primary"
        )

    if job_submit:
        skills = split_items(job_skills_text)

        if not skills:
            st.warning("Enter at least one skill.")
        else:
            try:
                jobs = match_jobs(
                    skills,
                    target_role.strip() or None,
                )

                if not jobs:
                    st.info(
                        "No matching sample opportunities were found. "
                        "Try different skills or a different role."
                    )

                for job in jobs:
                    with st.container(border=True):
                        st.subheader(
                            str(get_field(job, "title", "Opportunity"))
                        )
                        st.write(
                            f"**Company:** "
                            f"{get_field(job, 'company', 'Not specified')}"
                        )
                        st.write(
                            get_field(job, "description", "")
                        )

                        match_percent = get_field(
                            job, "match_percent", None
                        )
                        if match_percent is not None:
                            try:
                                percentage = float(match_percent)
                                st.metric(
                                    "Skill match",
                                    f"{percentage:.0f}%"
                                )
                                st.progress(
                                    max(0.0, min(1.0, percentage / 100))
                                )
                            except (TypeError, ValueError):
                                st.write(f"Skill match: {match_percent}")

                        matched = get_field(job, "matched_skills", [])
                        missing = get_field(job, "missing_skills", [])

                        st.write("**Matching skills:**")
                        st.write(
                            ", ".join(matched)
                            if matched else "No matching skills listed."
                        )

                        st.write("**Skills to learn:**")
                        st.write(
                            ", ".join(missing)
                            if missing else "No missing skills listed."
                        )

                        st.caption(
                            "Demonstration opportunity. Verify a vacancy "
                            "with an employer before applying."
                        )
            except Exception as error:
                show_error("Could not match opportunities.", error)


# --------------------------------------------------
# APPLICATION TRACKER
# --------------------------------------------------

elif selected_page == "Application Tracker":
    st.title("📋 Application Tracker")
    st.write(
        "Record your applications and review their status in one place."
    )

    with st.form("application_form"):
        company = st.text_input(
            "Company name",
            placeholder="DemoTech Solutions",
        )
        role = st.text_input(
            "Role",
            placeholder="Python Developer Intern",
        )
        status = st.selectbox(
            "Application status",
            ["Applied", "Under Review", "Interview", "Accepted", "Rejected"],
        )
        application_submit = st.form_submit_button(
            "Add Application", type="primary"
        )

    if application_submit:
        if not company.strip() or not role.strip():
            st.warning("Please enter both the company and role.")
        else:
            try:
                result = add_application(
                    user_id,
                    company.strip(),
                    role.strip(),
                    status,
                )
                success, message = result

                if success:
                    st.success(message)
                else:
                    st.error(message)
            except Exception as error:
                show_error("Could not add the application.", error)

    st.divider()
    st.subheader("Your applications")

    try:
        applications = get_user_applications(user_id) or []

        if not applications:
            st.info("You haven't recorded any applications yet.")
        else:
            for application in applications:
                with st.container(border=True):
                    st.subheader(
                        str(get_field(application, "role", "Application"))
                    )
                    st.write(
                        f"**Company:** "
                        f"{get_field(application, 'company', 'Not specified')}"
                    )
                    st.write(
                        f"**Status:** "
                        f"{get_field(application, 'status', 'Applied')}"
                    )
    except Exception as error:
        show_error("Could not load your applications.", error)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.sidebar.divider()
st.sidebar.caption("CareerPath AI • Student Project")
st.sidebar.caption("CareerPath AI • Student Project")
st.sidebar.caption("Plan your learning. Explore your future.")
