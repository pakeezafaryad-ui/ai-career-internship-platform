# AI Career and Internship Agent Platform

A university Software Engineering project starter for a secure career guidance and internship matching application.

## Current status

This repository currently contains the first runnable Streamlit interface and a Google Colab setup notebook. AI agents, authentication, database persistence, RAG, and notifications are not implemented yet.

**Demo mode:** The current page displays general learning suggestions only. It does not show real vacancies or guarantee career outcomes.

## Tech stack roadmap

- Python and Streamlit
- SQLite (with SQLAlchemy when database features are added)
- CrewAI and Groq for multi-agent workflows
- Hugging Face embeddings and ChromaDB for RAG
- n8n for optional reminders and notifications
- Git and GitHub for version control

## Run in Google Colab

1. Upload `AI_Career_Internship_Starter.ipynb` to Google Colab.
2. Run the cells from top to bottom.
3. The notebook installs Streamlit and checks the starter source files.
4. For interactive web preview in Colab, the notebook uses a temporary tunnel only if you explicitly run that optional cell. Do not enter passwords or upload sensitive CVs into a public demo.

## Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Upload to GitHub

1. Create a new empty GitHub repository.
2. Upload the project files, or use Git:
   ```bash
   git init
   git add .
   git commit -m "Add secure career platform starter"
   git branch -M main
   git remote add origin YOUR_REPOSITORY_URL
   git push -u origin main
   ```
3. Do not upload `.env`, API keys, private CVs, databases, or user records.

## Security principles for future steps

- Keep secrets out of source control; use Colab Secrets or Streamlit secrets.
- Enforce authentication and per-user authorization before storing private information.
- Treat uploaded documents and retrieved text as untrusted input.
- Validate AI outputs and require user approval before external actions.
- Use fictional sample listings only when clearly labeled as demo data.

## Planned build sequence

1. Starter interface and notebook
2. Configuration, dependencies, and secret handling
3. Database schema and authentication/authorization
4. CV parsing and structured validation
5. RAG ingestion and retrieval
6. Specialized agents and verification
7. Explainable job matching and roadmap tracking
8. Testing, privacy controls, and deletion/export
9. Optional n8n notifications
10. Deployment and final report
