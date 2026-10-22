
# AI Career and Internship Agent Platform

An educational career guidance platform built with Python and Streamlit. It helps students explore career paths, identify skill gaps, create learning roadmaps, discover sample opportunities, and track internship applications.

## Features

- **Career Advisor:** Recommends career paths based on interests and skills.
- **Skill Gap Analyzer:** Compares existing skills with career requirements.
- **Learning Roadmaps:** Creates structured learning plans for selected careers.
- **Opportunity Matcher:** Matches skills against a sample job and internship dataset.
- **Application Tracker:** Records applications and tracks their status.
- **User Accounts:** Supports registration and login with hashed passwords.
- **Privacy and Safety:** Separates user records by account and avoids storing plain-text passwords.

## Technology Stack

- Python
- Streamlit
- SQLAlchemy
- SQLite
- Argon2 password hashing
- JSON sample dataset
- GitHub
- Streamlit Community Cloud

## Project Structure

```text
ai-career-internship-platform/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── sample_jobs.json
└── services/
    ├── __init__.py
    ├── database.py
    ├── auth_service.py
    ├── career_advisor.py
    ├── skill_gap.py
    ├── learning_roadmap.py
    ├── job_matcher.py
    └── application_tracker.py
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/pakeezafaryad-ui/ai-career-internship-platform.git
cd ai-career-internship-platform
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app.py
```

The terminal will provide a local URL where you can open the application.

## Privacy and Security

- Passwords are hashed instead of stored as plain text.
- Database queries should restrict records to the authenticated user.
- Secrets and environment files should not be committed to GitHub.
- Use fictional data when demonstrating the project.
- Do not enter sensitive personal information into a demonstration deployment.
- Sample opportunities are fictional and must not be treated as verified vacancies.

## Current Limitations

This is an educational prototype. Career recommendations and skill matching use rule-based logic rather than a trained AI model. Job listings are sample data, not live vacancies. The platform does not guarantee employment, internship placement, or career outcomes.

Before production use, add appropriate session protection, login rate limiting, email verification, database backup and retention policies, and further security testing.

## Future Improvements

- Integrate verified job and internship sources.
- Add retrieval-augmented generation (RAG) for career resources.
- Introduce a multi-agent career guidance workflow.
- Add email notifications and application reminders.
- Add administrator tools and stronger access controls.
- Deploy with persistent database storage and monitoring.

## Author

**Pakeeza Faryad**

Software Engineering Student

GitHub: https://github.com/pakeezafaryad-ui

---

*Created as an educational project to explore career guidance, automation, and secure web application development.*
