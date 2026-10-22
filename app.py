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
    page_title="AI Career & Internship Agent",
    page_icon="🎓",
    layout="wide",
)

# Initialize the database
try:
    init_db()
except Exception as exc:
    st.error("Could not initialize the database.")
    st.exception(exc)
    st.stop()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def split_items(value):
    """Convert comma-separated text into a list."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def show_value(value):
    """Display returned service data safely."""
    if isinstance(value, dict):
        for key, item in value.items():
            st.write(f"**{str(key).replace('_', ' ').title()}:**")
            if isinstance(item, (dict, list)):
                st.json(item, expanded=False)
            else:
                st.write(item)
    elif isinstance(value, (list, tuple)):
        if not value:
            st.info("No results found yet.")
        else:
            for item in value:
                if isinstance(item, dict):
                    with st.container(border=True):
                        show_value(item)
                else:
                    st.write(item)
    else:
        st.write(value)


def get_field(item, *names, default=None):
    """Read a field from a dictionary without raising KeyError."""
    if not isinstance(item, dict):
        return default
    for name in names:
        if name in item:
            return item[name]
    return default


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 AI Career & Internship Agent")
st.caption(
    "Explore career paths, identify skill gaps, build learning plans, "
    "match sample jobs, and track applications."
)


# --------------------------------------------------
# LOGIN AND REGISTRATION
# --------------------------------------------------

if st.session_state.user is None:
    login_tab, register_tab = st.tabs(["Login", "Create Account"])

    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )
            login_submit = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if login_submit:
            if not login_email.strip() or not login_password:
                st.warning("Enter your email and password.")
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
                except Exception:
                    st.error("Login failed. Please try again.")

    with register_tab:
        st.subheader("Create your account")

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
                key="confirm_password",
            )
            register_submit = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if register_submit:
            email = new_email.strip().lower()

            if not email or "@" not in email:
                st.warning("Enter a valid email address.")
            elif len(new_password) < 8:
                st.warning("Use a password with at least 8 characters.")
            elif new_password != confirm_password:
                st.error("The passwords do not match.")
            else:
                try:
                    success, message = register_user(email, new_password)
                    if success:
                        st.success(message)
                        st.info("You can now log in using your new account.")
                    else:
                        st.error(message)
                except Exception:
                    st.error("Registration failed. Please try again.")

    st.info("Create an account or log in to access your career dashboard.")
    st.stop()


# --------------------------------------------------
# AUTHENTICATED DASHBOARD
# --------------------------------------------------

user = st.session_state.user
user_id = user["id"]

with st.sidebar:
    st.title("Your Dashboard")
    st.write(f"Logged in as **{user.get('email', 'User')}**")
    st.divider()

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()

    st.caption("AI Career & Internship Agent")
    st.caption("Opportunities in this version include sample listings.")


career_tab, skills_tab, roadmap_tab, jobs_tab, tracker_tab = st.tabs(
    [
        "Career Advisor",
        "Skill Gap",
        "Learning Roadmap",
        "Job Matcher",
        "Application Tracker",
    ]
)


# --------------------------------------------------
# 1. CAREER ADVISOR
# --------------------------------------------------

with career_tab:
    st.header("Find Suitable Career Paths")
    st.write("Tell us about your interests, skills, and career goal.")

    with st.form("career_form"):
        interests_text = st.text_input(
            "Your interests",
            placeholder="Artificial Intelligence, programming, automation",
        )
        skills_text = st.text_input(
            "Your current skills",
            placeholder="Python, Java, Git and GitHub",
        )
        career_goal = st.text_input(
            "Your target career",
            placeholder="AI Engineer",
        )
        career_submit = st.form_submit_button("Find Career Paths")

    if career_submit:
        interests = split_items(interests_text)
        skills = split_items(skills_text)

        try:
            results = recommend_careers(
                interests,
                skills,
                career_goal,
            )

            if not results:
                st.info("No exact match found. Try adding more interests or skills.")
            else:
                for item in results:
                    if not isinstance(item, dict):
                        st.write(item)
                        continue

                    title = get_field(
                        item, "career", "title", "name",
                        default="Suggested Career",
                    )
                    with st.container(border=True):
                        st.subheader(str(title))

                        description = get_field(item, "description")
                        if description:
                            st.write(description)

                        reason = get_field(
                            item,
                            "reason",
                            "explanation",
                            default="Recommended based on your interests and skills.",
                        )
                        st.write(f"**Why this career?** {reason}")

                        required_skills = get_field(
                            item, "skills", "required_skills",
                        )
                        if required_skills:
                            st.write("**Skills to develop:**")
                            if isinstance(required_skills, list):
                                st.write(", ".join(map(str, required_skills)))
                            else:
                                st.write(required_skills)

                        matched_skills = get_field(item, "matched_skills")
                        if matched_skills:
                            st.write("**Matching skills:**")
                            st.write(matched_skills)

        except Exception as exc:
            st.error("Could not generate career recommendations.")
            st.exception(exc)


# --------------------------------------------------
# 2. SKILL GAP ANALYZER
# --------------------------------------------------

with skills_tab:
    st.header("Skill Gap Analyzer")
    st.write("Compare your current skills with a target career.")

    with st.form("skill_gap_form"):
        current_skills_text = st.text_input(
            "Current skills",
            placeholder="Python, Pandas",
        )
        target_career = st.selectbox(
            "Target career",
            [
                "AI Engineer",
                "Python Developer",
                "Web Developer",
                "Data Analyst",
                "Cybersecurity Analyst",
                "Java Developer",
                "UI/UX Designer",
            ],
        )
        skill_submit = st.form_submit_button("Analyze Skill Gap")

    if skill_submit:
        current_skills = split_items(current_skills_text)

        try:
            result = analyze_skill_gap(current_skills, target_career)
            st.subheader("Your Skill Gap Results")
            show_value(result)
        except Exception as exc:
            st.error("Could not analyze your skills.")
            st.exception(exc)


# --------------------------------------------------
# 3. LEARNING ROADMAP
# --------------------------------------------------

with roadmap_tab:
    st.header("Personalized Learning Roadmap")
    st.write("Generate a learning plan for your chosen career.")

    with st.form("roadmap_form"):
        roadmap_career = st.selectbox(
            "Career goal",
            [
                "AI Engineer",
                "Python Developer",
                "Web Developer",
                "Data Analyst",
                "Cybersecurity Analyst",
                "Java Developer",
            ],
        )
        roadmap_skills_text = st.text_input(
            "Skills you already know",
            placeholder="Python, Java",
        )
        duration = st.slider(
            "Roadmap duration (weeks)",
            min_value=4,
            max_value=24,
            value=8,
            step=4,
        )
        roadmap_submit = st.form_submit_button("Generate Roadmap")

    if roadmap_submit:
        current_skills = split_items(roadmap_skills_text)

        try:
            roadmap = generate_learning_roadmap(
                roadmap_career,
                current_skills,
                duration,
            )

            st.session_state.generated_roadmap = roadmap
            st.session_state.roadmap_saved = False

            st.subheader(f"{duration}-Week Plan")
            show_value(roadmap)

        except Exception as exc:
            st.error("Could not generate the learning roadmap.")
            st.exception(exc)

    if "generated_roadmap" in st.session_state:
        if st.button("Save Roadmap to My Account"):
            try:
                success = save_roadmap(
                    user_id,
                    st.session_state.generated_roadmap,
                )

                if success:
                    st.success("Roadmap saved successfully.")
                else:
                    st.error("The roadmap could not be saved.")

            except Exception as exc:
                st.error("Could not save the roadmap.")
                st.exception(exc)

    st.divider()
    st.subheader("My Saved Roadmaps")

    try:
        saved_roadmaps = get_user_roadmaps(user_id)
        if saved_roadmaps:
            show_value(saved_roadmaps)
        else:
            st.info("You have not saved any roadmaps yet.")
    except Exception as exc:
        st.error("Could not load saved roadmaps.")
        st.exception(exc)


# --------------------------------------------------
# 4. JOB MATCHER
# --------------------------------------------------

with jobs_tab:
    st.header("Job & Internship Matcher")
    st.write(
        "Find sample opportunities that match your skills. "
        "These listings are for demonstration and are not verified live vacancies."
    )

    with st.form("job_match_form"):
        job_skills_text = st.text_input(
            "Your skills",
            placeholder="Python, SQL, Git and GitHub, REST APIs",
        )
        target_role = st.text_input(
            "Preferred role (optional)",
            placeholder="Python Developer Intern",
        )
        job_submit = st.form_submit_button("Find Matching Jobs")

    if job_submit:
        user_skills = split_items(job_skills_text)

        try:
            jobs = match_jobs(
                user_skills,
                target_role.strip() or None,
            )

            if not jobs:
                st.info("No matching sample jobs found. Try different skills.")
            else:
                for job in jobs:
                    if not isinstance(job, dict):
                        st.write(job)
                        continue

                    title = get_field(job, "title", default="Opportunity")
                    company = get_field(job, "company", default="Company not specified")

                    with st.container(border=True):
                        st.subheader(str(title))
                        st.write(f"**Company:** {company}")

                        description = get_field(job, "description")
                        if description:
                            st.write(description)

                        match_percent = get_field(job, "match_percent")
                        if match_percent is not None:
                            st.metric("Skill Match", f"{match_percent}%")

                        matched = get_field(job, "matched_skills", default=[])
                        missing = get_field(job, "missing_skills", default=[])

                        if matched:
                            st.write("**Matching skills:**", ", ".join(map(str, matched)))
                        if missing:
                            st.write("**Skills to learn:**", ", ".join(map(str, missing)))

                        application_url = get_field(job, "application_url")
                        if application_url and str(application_url).startswith(("https://", "http://")):
                            st.link_button("Open Opportunity", application_url)
                        else:
                            st.caption("Sample listing — no live application link.")

        except Exception as exc:
            st.error("Could not match jobs.")
            st.exception(exc)


# --------------------------------------------------
# 5. APPLICATION TRACKER
# --------------------------------------------------

with tracker_tab:
    st.header("Application Tracker")
    st.write("Record and review your internship or job applications.")

    with st.form("application_form"):
        company = st.text_input(
            "Company",
            placeholder="DemoTech Solutions",
        )
        role = st.text_input(
            "Job or internship role",
            placeholder="Python Developer Intern",
        )
        status = st.selectbox(
            "Application status",
            [
                "Interested",
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected",
            ],
        )
        application_submit = st.form_submit_button("Add Application")

    if application_submit:
        if not company.strip() or not role.strip():
            st.warning("Enter both the company and role.")
        else:
            try:
                success, message = add_application(
                    user_id,
                    company.strip(),
                    role.strip(),
                    status,
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

            except Exception as exc:
                st.error("Could not add the application.")
                st.exception(exc)

    st.divider()
    st.subheader("My Applications")

    try:
        applications = get_user_applications(user_id)

        if applications:
            show_value(applications)
        else:
            st.info("No applications recorded yet.")

    except Exception as exc:
        st.error("Could not load your applications.")
        st.exception(exc)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "AI Career & Internship Agent Platform | "
    "Career suggestions are guidance, not guarantees. "
    "Sample job listings must be independently verified."
)
