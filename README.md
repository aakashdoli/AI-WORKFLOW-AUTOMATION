# AI Workflow Automation Platform

A production-style internal operations system that automates repetitive business workflows using LLMs, structured business data, and lightweight dashboards.

## Features
- **AI-Powered Report Analysis**: CSV ingestion and automated insight extraction.
- **Classification Pipeline**: Categorize tickets, feedback, and incidents.
- **Executive Summaries**: AI-generated operational reports.
- **Monitoring Dashboard**: Streamlit-based UI for workflow visibility.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your `GEMINI_API_KEY`.

3. **Run the dashboard**:
   ```bash
   streamlit run app/dashboard/streamlit_app.py
   ```

## Architecture
- **Backend**: Python, SQLAlchemy, SQLite.
- **AI**: Gemini API via `google-genai`.
- **UI**: Streamlit.
