import streamlit as st

st.set_page_config(
    page_title="AI Career & Internship Agent",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI Career and Internship Agent Platform")
st.caption("A secure, multi-agent career guidance and internship matching project")

st.info(
    "Starter version: this interface is a demo only. It does not yet create accounts, "
    "process private CVs, call AI models, or retrieve live vacancies."
)

st.subheader("Project modules")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📄 CV Analyzer")
    st.write("Planned: extract CV details and identify skills.")

with col2:
    st.markdown("### 🧭 Career Advisor")
    st.write("Planned: recommend career paths with explanations.")

with col3:
    st.markdown("### 💼 Job Matcher")
    st.write("Planned: compare skills with job requirements.")

st.subheader("Try the demo")
interest = st.selectbox(
    "Which area interests you most?",
    ["AI / Machine Learning", "Software Development", "Cybersecurity", "Data Analytics", "UI/UX Design"],
)
if st.button("Show starter guidance"):
    guidance = {
        "AI / Machine Learning": "Start with Python, data handling, basic statistics, and small ML projects.",
        "Software Development": "Practice programming fundamentals, Git, testing, data structures, and one portfolio project.",
        "Cybersecurity": "Learn networking, operating-system basics, security principles, and legal lab-based practice.",
        "Data Analytics": "Start with spreadsheets, SQL, Python or a BI tool, and data visualization.",
        "UI/UX Design": "Practice user research, wireframes, accessibility, prototyping, and portfolio case studies.",
    }
    st.success(guidance[interest])

st.divider()
st.caption("Demo content only. Recommendations are general learning suggestions, not guarantees of employment.")
