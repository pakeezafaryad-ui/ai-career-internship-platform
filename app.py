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
    page_title="Career Compass",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# --------------------------------------------------
# SIMPLE, ATTRACTIVE DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7ff;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #342b82, #6555d9);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #f0efff;
        font-size: 16px;
    }

    .result-card {
        background: white;
        border: 1px solid #e4e7f5;
        border-radius: 14px;
        padding: 20px;
        margin: 12px 0;
    }

    .small-label {
        color: #686b80;
        font-size: 13px;
    }

    h2, h3 {
        color: #29265b;
    }

    div.stButton > button[kind="primary"] {
        background: #5145cd;
        border-color: #5145cd;
        color: white;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def split_items(value):
    """Convert comma-separated text into a clean list."""
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def show_list(items, empty_message="Nothing to show yet."):
    if not items:
        st.info(empty_message)
        return

    for item in items:
        st.write(f"• {item}")


def get_value(item, *keys, default="Not provided"):
    """Read a dictionary value without causing KeyError."""
    if not isinstance(item, dict):
        return default

    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value

    return default


def show_career_recommendations(recommendations):
    if not recommendations:
        st.info(
            "No career matches found. Try adding more skills "
            "or interests."
        )
        return

    for number, item in enumerate(recommendations, start=1):
        career = get_value(
            item, "career", "title", "name",
            default="Career option"
        )
        description = get_value(
            item, "description", "overview",
            default="Explore this career to learn more."
        )
        reason = get_value(
            item, "reason", "why", "explanation",
            default=(
                "This career may be worth exploring "
                "based on your information."
            )
        )
        matching = get_value(
            item, "matching_skills", "matched_skills", "skills",
            default=[]
        )

        with st.container(border=True):
            st.subheader(f"{number}. {career}")
            st.write(description)
            st.markdown(f"**Why it may suit you:** {reason}")

            if isinstance(matching, list):
                st.markdown("**Relevant skills:**")
                show_list(matching, "Build relevant skills for this career.")
            elif matching != "Not provided":
                st.write(f"**Relevant skills:** {matching}")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🎯 Career Compass")
    st.caption("Your career and internship companion")

    if st.session_state.user:
        st.success(
            f"Signed in as {st.session_state.user['email']}"
        )
        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Career Advisor",
                "Skill Gap Analyzer",
                "Learning Roadmap",
                "Find Internships",
                "Application Tracker",
                "My Profile",
            ],
        )

        if st.button("Log out", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        page = "Welcome"


# --------------------------------------------------
# WELCOME / LOGIN / REGISTRATION
# --------------------------------------------------

if not st.session_state.user:
    st.markdown(
        """
        <div class="hero">
            <h1>🎯 Find your next career move</h1>
            <p>
                Discover career paths, identify skills to learn,
                build a roadmap, and organize your applications.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Log in", "✨ Create account"]
    )

    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            login_email = st.text_input("Email address")
            login_password = st.text_input(
                "Password", type="password"
            )
            login_submit = st.form_submit_button(
                "Log in", type="primary",
                use_container_width=True
            )

        if login_submit:
            if not login_email.strip() or not login_password:
                st.warning("Enter both email and password.")
            else:
                try:
                    user = authenticate_user(
                        login_email.strip().lower(),
                        login_password,
                    )

                    if user:
                        st.session_state.user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(
                            "Login failed. Check your details "
                            "or create an account."
                        )
                except Exception as error:
                    st.error(f"Could not log in: {error}")

    with register_tab:
        st.subheader("Create your account")

        with st.form("register_form"):
            register_email = st.text_input(
                "Email address", key="register_email"
            )
            register_password = st.text_input(
                "Create password",
                type="password",
                key="register_password",
            )
            confirm_password = st.text_input(
                "Confirm password", type="password"
            )
            register_submit = st.form_submit_button(
                "Create account",
                type="primary",
                use_container_width=True,
            )

        if register_submit:
            email = register_email.strip().lower()

            if not email or "@" not in email:
                st.warning("Enter a valid email address.")
            elif len(register_password) < 8:
                st.warning(
                    "Use a password with at least 8 characters."
                )
            elif register_password != confirm_password:
                st.warning("The passwords do not match.")
            else:
                try:
                    result = register_user(email, register_password)

                    if isinstance(result, tuple):
                        success, message = result
                    else:
                        success = bool(result)
                        message = (
                            "Account created."
                            if success else "Could not create account."
                        )

                    if success:
                        st.success(
                            f"{message} You can now log in."
                        )
                    else:
                        st.error(str(message))
                except Exception as error:
                    st.error(f"Registration failed: {error}")

    st.stop()


# --------------------------------------------------
# LOGGED-IN USER
# --------------------------------------------------

user_id = st.session_state.user.get("id")
user_email = st.session_state.user.get("email", "User")

st.markdown(
    f"""
    <div class="hero">
        <h1>Welcome to Career Compass 👋</h1>
        <p>
            Make your next career step with a clear plan.
            Signed in as {user_email}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":
    st.subheader("Your career dashboard")

    col1, col2, col3 = st.columns(3)

    try:
        applications = get_user_applications(user_id) or []
    except Exception:
        applications = []

    try:
        roadmaps = get_user_roadmaps(user_id) or []
    except Exception:
        roadmaps = []

    with col1:
        st.metric("📨 Applications", len(applications))

    with col2:
        st.metric("🗺️ Learning roadmaps", len(roadmaps))

    with col3:
        st.metric("🚀 Career tools", 5)

    st.markdown("### Start here")

    st.write(
        "1. Get career suggestions based on your interests and skills."
    )
    st.write(
        "2. Identify the skills you need for your target career."
    )
    st.write(
        "3. Create a learning roadmap and find sample internships."
    )

    st.info(
        "Tip: Start with Career Advisor, then use Skill Gap Analyzer "
        "to decide what to learn next."
    )


# --------------------------------------------------
# CAREER ADVISOR
# --------------------------------------------------

elif page == "Career Advisor":
    st.subheader("🧭 Find suitable career paths")
    st.write(
        "Tell us what you enjoy and what you can do. "
        "We will suggest careers worth exploring."
    )

    with st.form("career_form"):
        interests_text = st.text_area(
            "Your interests",
            placeholder="Example: AI, programming, automation",
        )
        skills_text = st.text_area(
            "Your current skills",
            placeholder="Example: Python, Java, Git",
        )
        career_goal = st.text_input(
            "Career goal (optional)",
            placeholder="Example: AI Engineer",
        )

        submitted = st.form_submit_button(
            "Find my career matches",
            type="primary",
        )

    if submitted:
        interests = split_items(interests_text)
        skills = split_items(skills_text)

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
                st.markdown("### Your suggested career paths")
                show_career_recommendations(recommendations)
            except Exception as error:
                st.error(
                    "Could not generate career recommendations. "
                    "Check services/career_advisor.py."
                )
                st.caption(str(error))


# --------------------------------------------------
# SKILL GAP ANALYZER
# --------------------------------------------------

elif page == "Skill Gap Analyzer":
    st.subheader("🧩 Discover which skills to learn next")
    st.write(
        "Compare your current skills with a target career."
    )

    with st.form("skill_gap_form"):
        current_skills_text = st.text_input(
            "Your current skills",
            placeholder="Python, Java, SQL",
        )
        target_career = st.selectbox(
            "Target career",
            [
                "AI Engineer",
                "Python Developer",
                "Web Developer",
                "Data Analyst",
                "Cybersecurity Analyst",
                "Software Engineer",
            ],
        )
        gap_submit = st.form_submit_button(
            "Analyze my skills",
            type="primary",
        )

    if gap_submit:
        skills = split_items(current_skills_text)

        if not skills:
            st.warning("Enter at least one current skill.")
        else:
            try:
                result = analyze_skill_gap(skills, target_career)

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
                        result.get("match_percent", None),
                    )

                    st.markdown("### Your results")

                    if percentage is not None:
                        try:
                            st.metric(
                                "Current skill match",
                                f"{float(percentage):.0f}%",
                            )
                            st.progress(
                                max(0.0, min(1.0, float(percentage) / 100))
                            )
                        except (ValueError, TypeError):
                            pass

                    left, right = st.columns(2)

                    with left:
                        st.markdown("#### ✅ Skills you have")
                        show_list(
                            matched if isinstance(matched, list) else [],
                            "No matching skills identified yet.",
                        )

                    with right:
                        st.markdown("#### 📚 Skills to learn")
                        show_list(
                            missing if isinstance(missing, list) else [],
                            "No missing skills were returned.",
                        )

                    if not matched and not missing:
                        st.write("Full analysis:")
                        st.write(result)
                else:
                    st.write(result)

            except Exception as error:
                st.error("The skill-gap analysis could not be completed.")
                st.caption(str(error))


# --------------------------------------------------
# LEARNING ROADMAP
# --------------------------------------------------

elif page == "Learning Roadmap":
    st.subheader("🗺️ Build your learning plan")
    st.write(
        "Create a manageable plan to move toward your chosen career."
    )

    with st.form("roadmap_form"):
        roadmap_career = st.selectbox(
            "What do you want to become?",
            [
                "Python Developer",
                "AI Engineer",
                "Web Developer",
                "Data Analyst",
                "Cybersecurity Analyst",
                "Software Engineer",
            ],
        )
        roadmap_skills_text = st.text_input(
            "Skills you already know",
            placeholder="Python, Java",
        )
        weeks = st.slider(
            "How many weeks do you have?",
            min_value=4,
            max_value=24,
            value=8,
            step=4,
        )
        roadmap_submit = st.form_submit_button(
            "Create my roadmap",
            type="primary",
        )

    if roadmap_submit:
        current_skills = split_items(roadmap_skills_text)

        try:
            roadmap = generate_learning_roadmap(
                roadmap_career,
                current_skills,
                weeks,
            )

            st.markdown("### Your learning roadmap")

            if isinstance(roadmap, dict):
                title = roadmap.get("title", roadmap_career)
                st.markdown(f"#### {title}")

                plan = roadmap.get(
                    "plan",
                    roadmap.get("weeks", roadmap.get("roadmap", [])),
                )

                if isinstance(plan, list):
                    for index, step in enumerate(plan, start=1):
                        with st.container(border=True):
                            if isinstance(step, dict):
                                heading = get_value(
                                    step, "week", "title", "topic",
                                    default=f"Step {index}",
                                )
                                details = get_value(
                                    step, "tasks", "description",
                                    "activities", "content",
                                    default="Work through this learning step.",
                                )
                                st.markdown(f"**{heading}**")
                                if isinstance(details, list):
                                    show_list(details)
                                else:
                                    st.write(details)
                            else:
                                st.write(f"**Step {index}:** {step}")
                elif isinstance(plan, str):
                    st.write(plan)
                else:
                    st.write(roadmap)

            elif isinstance(roadmap, list):
                for index, step in enumerate(roadmap, start=1):
                    st.markdown(f"**Step {index}**")
                    st.write(step)
            else:
                st.write(roadmap)

            if st.button("Save this roadmap", type="primary"):
                saved = save_roadmap(user_id, roadmap)
                if saved:
                    st.success("Roadmap saved to your account.")
                else:
                    st.warning(
                        "The save function did not confirm success. "
                        "Check services/learning_roadmap.py."
                    )

        except Exception as error:
            st.error("Could not create the learning roadmap.")
            st.caption(str(error))

    st.markdown("### Previously saved roadmaps")

    try:
        saved_roadmaps = get_user_roadmaps(user_id) or []

        if not saved_roadmaps:
            st.info("Your saved roadmaps will appear here.")
        else:
            for item in saved_roadmaps:
                with st.container(border=True):
                    st.markdown(
                        f"**{get_value(item, 'title', default='Learning roadmap')}**"
                    )
                    st.write(
                        get_value(
                            item, "plan",
                            default="Open your roadmap to view the plan.",
                        )
                    )
                    progress = item.get("progress_percent", 0)
