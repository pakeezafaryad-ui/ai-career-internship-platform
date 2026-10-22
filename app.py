
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


def csv_items(text):
    """Convert comma-separated text into a list."""
    return [item.strip() for item in text.split(",") if item.strip()]


st.set_page_config(
    page_title="AI Career & Internship Agent",
    page_icon="🎓",
    layout="wide",
)

init_db()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 AI Career and Internship Agent Platform")
st.caption(
    "Explore career paths, identify skill gaps, plan learning, "
    "and organize internship applications."
)

# ---------------- ACCOUNT SIDEBAR ----------------

with st.sidebar:
    st.header("Account")

    if st.session_state.user:
        st.success(f"Signed in: {st.session_state.user['email']}")

        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()

    else:
        account_mode = st.radio(
            "Choose an option",
            ["Login", "Register"],
        )

        email = st.text_input("Email address")
        password = st.text_input(
            "Password (minimum 12 characters for registration)",
            type="password",
        )

        if st.button(account_mode):
            if account_mode == "Register":
                try:
                    success, message = register_user(email, password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                except Exception:
                    st.error("Registration failed. Please check your input.")

            else:
                user = authenticate_user(email, password)

                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

# ---------------- WELCOME PAGE ----------------

if not st.session_state.user:
    st.info("Register or log in using the sidebar to access your workspace.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Career Planning")
        st.write(
            "- Career recommendations\n"
            "- Skill-gap analysis\n"
            "- Personalized learning roadmaps"
        )

    with col2:
        st.subheader("Internship Preparation")
        st.write(
            "- Demonstration opportunity matching\n"
            "- Application tracking\n"
            "- Learning resource links"
        )

    st.warning(
        "Educational prototype: use a unique password and do not enter "
        "sensitive personal information."
    )
    st.stop()

user_id = st.session_state.user["id"]

# ---------------- MAIN WORKSPACE ----------------

career_tab, skill_tab, roadmap_tab, jobs_tab, tracker_tab, privacy_tab = (
    st.tabs(
        [
            "Career Advisor",
            "Skill Gap",
            "Learning Roadmap",
            "Opportunities",
            "Application Tracker",
            "Privacy & Safety",
        ]
    )
)

# ---------------- CAREER ADVISOR ----------------

with career_tab:
    st.subheader("Find Suitable Career Paths")

    interests = st.text_input(
        "Your interests",
        placeholder="AI, Python, web development",
    )

    current_skills = st.text_input(
        "Your current skills",
        placeholder="Python, Java, HTML",
    )

    if st.button("Recommend Careers"):
        recommendations = recommend_careers(
            csv_items(interests),
            csv_items(current_skills),
        )

        if recommendations:
            for item in recommendations:
                st.markdown(f"### {item['career']}")
                st.write(item["reason"])
        else:
            st.info("No recommendations are available yet.")

# ---------------- SKILL GAP ----------------

with skill_tab:
    st.subheader("Analyze Your Skill Gap")

    target_career = st.selectbox(
        "Choose your target career",
        [
            "AI Engineer",
            "Python Developer",
            "Web Developer",
            "Data Analyst",
            "Cybersecurity Analyst",
            "Java Developer",
        ],
    )

    existing_skills = st.text_input(
        "Skills you already know",
        placeholder="Python, Java, SQL",
        key="skill_gap_input",
    )

    if st.button("Analyze Skill Gap"):
        result = analyze_skill_gap(
            target_career,
            csv_items(existing_skills),
        )

        st.metric(
            "Estimated skill match",
            f"{result['match_percent']}%",
        )

        st.write("#### Skills you already have")
        if result["matched_skills"]:
            st.write(", ".join(result["matched_skills"]))
        else:
            st.write("No matching skills entered yet.")

        st.write("#### Skills to learn")
        if result["gaps"]:
            for gap in result["gaps"]:
                st.write(f"- {gap['skill']} — {gap['level']}")
        else:
            st.success("You match all the listed target skills.")

# ---------------- LEARNING ROADMAP ----------------

with roadmap_tab:
    st.subheader("Create a Learning Roadmap")

    roadmap_career = st.selectbox(
        "Your learning goal",
        [
            "AI Engineer",
            "Python Developer",
            "Web Developer",
            "Data Analyst",
            "Java Developer",
        ],
    )

    roadmap_skills = st.text_input(
        "Your existing skills",
        placeholder="Python, HTML",
        key="roadmap_skills_input",
    )

    if st.button("Generate and Save Roadmap"):
        try:
            plan = generate_learning_roadmap(
                roadmap_career,
                csv_items(roadmap_skills),
            )

            roadmap_id = save_roadmap(user_id, plan)
            st.session_state["latest_roadmap"] = plan

            st.success(f"Roadmap saved successfully. ID: {roadmap_id}")

        except Exception as error:
            st.error(f"Could not save roadmap: {error}")

    plan = st.session_state.get("latest_roadmap")

    if plan:
        st.write(f"**Goal:** {plan['career']}")
        st.write(plan["message"])
        st.progress(plan["match_percent"] / 100)

        for step in plan["roadmap"]:
            st.markdown(f"**Step {step['step']}: {step['skill']}**")
            st.write(step["task"])
            st.link_button(
                f"Learn {step['skill']}",
                step["resource"],
            )

    st.write("#### Previously Saved Roadmaps")

    try:
        saved_roadmaps = get_user_roadmaps(user_id)

        if not saved_roadmaps:
            st.caption("You have not saved any roadmaps yet.")

        for saved in saved_roadmaps:
            with st.expander(saved["title"]):
                st.write(
                    "Progress:",
                    f"{saved['progress_percent']}%",
                )
                st.json(saved["plan"])

    except Exception as error:
        st.error(f"Could not load roadmaps: {error}")

# ---------------- OPPORTUNITY MATCHING ----------------

with jobs_tab:
    st.subheader("Find Matching Opportunities")

    st.info(
        "This version uses fictional demonstration listings. "
        "It does not search or verify live vacancies."
    )

    job_skills = st.text_input(
        "Your skills",
        placeholder="Python, Git, SQL",
        key="job_skills_input",
    )

    if st.button("Find Matching Opportunities"):
        try:
            matches = match_jobs(csv_items(job_skills))

            if not matches:
                st.info(
                    "No demonstration listings matched. "
                    "Try entering more skills."
                )

            for job in matches:
                with st.container(border=True):
                    st.markdown(
                        f"### {job['title']} — {job['company']}"
                    )
                    st.write(job["description"])
                    st.write("Skills:", ", ".join(job["skills"]))
                    st.write(
                        "Estimated match:",
                        f"{job['match_percent']}%",
                    )

        except Exception as error:
            st.error(f"Matching failed: {error}")

# ---------------- APPLICATION TRACKER ----------------

with tracker_tab:
    st.subheader("Track Your Applications")

    with st.form("application_form"):
        company = st.text_input("Company name")
        role = st.text_input("Job or internship title")

        status = st.selectbox(
            "Application status",
            [
                "Interested",
                "Applied",
                "Interview",
                "Rejected",
                "Offer",
            ],
        )

        submitted = st.form_submit_button("Save Application")

    if submitted:
        try:
            add_application(
                user_id,
                company,
                role,
                status,
            )
            st.success("Application saved.")

        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Could not save the application.")

    st.write("#### Your Applications")

    try:
        applications = get_user_applications(user_id)

        if not applications:
            st.caption("No applications recorded yet.")

        for application in applications:
            st.write(
                f"**{application['role']}** at "
                f"{application['company']} — "
                f"{application['status']}"
            )

    except Exception as error:
        st.error(f"Could not load applications: {error}")

# ---------------- PRIVACY & SAFETY ----------------

with privacy_tab:
    st.subheader("Privacy and Safety")

    st.write("- Passwords are hashed rather than stored as plain text.")
    st.write("- Use a unique password for this student project.")
    st.write("- Do not submit identity documents or sensitive personal data.")
    st.write("- Your roadmaps and applications are associated with your account.")
    st.write("- This prototype uses SQLite; hosted data may not persist after redeployment.")
    st.write("- Demo listings are fictional and are not real job offers.")
    st.write("- Live AI APIs and multi-agent orchestration are not enabled in this version.")
