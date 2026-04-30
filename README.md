# AI Ops Automation Platform ⚡

A production-grade AI Workflow Automation and Orchestration Platform designed for enterprise-level operational efficiency. This platform leverages Large Language Models (LLMs), asynchronous task processing, and a robust microservice architecture to automate complex business workflows.

[![AI Ops CI/CD](https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION/actions/workflows/main.yml/badge.svg)](https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🏗️ Architecture Overview

The platform is designed with a decoupled microservice architecture:

- **Frontend**: Streamlit Dashboard for real-time monitoring and triggering workflows.
- **Backend**: FastAPI REST API handling execution requests and history.
- **Async Engine**: Celery + Redis for managing long-running AI pipelines without blocking the UI.
- **AI Core**: Gemini AI (via `google-genai`) providing structured reasoning and classification.
- **Data Layer**: SQLAlchemy (PostgreSQL/SQLite) tracking execution metrics, latency, and token usage.

```text
Streamlit Dashboard  <--->  FastAPI Backend  <--->  Redis Queue  <--->  Celery Workers
                                 |                                        |
                          SQLAlchemy (DB) <----------------------- AI Pipelines (Gemini)
```

---

## 🚀 Key Features

### 1. Intelligent Business Pipelines
- **Customer Support Automation**: High-accuracy ticket classification and escalation routing.
- **Financial Fraud Detection**: Anomaly detection in transactions with AI-generated reasoning.
- **Executive KPI Reporting**: Management-level summaries generated from raw operational data.

### 2. Operational Visibility
- **Real-time Analytics**: Plotly charts for latency trends, token usage, and volume distribution.
- **Structured Logging**: JSON-formatted logs for production tracing and debugging.
- **Execution History**: Comprehensive audit trails of every AI decision.

### 3. Production Engineering
- **Asynchronous Processing**: Background task execution via Celery.
- **Full Dockerization**: Containerized environment for local development and cloud deployment.
- **CI/CD Ready**: Automated testing and linting via GitHub Actions.

---

## 🛠️ Installation & Setup

### Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION.git
   cd AI-WORKFLOW-AUTOMATION
   ```
2. Configure `.env`:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY
   ```
3. Launch the platform:
   ```bash
   docker-compose up --build
   ```

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis: `brew install redis && brew services start redis`
3. Start FastAPI: `uvicorn app.api.main:app --reload`
4. Start Celery Worker: `celery -A app.tasks worker --loglevel=info`
5. Start Dashboard: `streamlit run app/dashboard/streamlit_app.py`

---

## 📊 Sample Workflows

| Workflow | Input | Output |
| :--- | :--- | :--- |
| **Fraud Analysis** | `transactions.csv` | Risk Level, Anomaly Explanation, Confidence Score |
| **KPI Reporting** | `metrics.csv` | Management Summary, Strategy Recommendations |
| **Ticket Ops** | `tickets.csv` | Category, Priority, Escalation Logic |

---

## 🛡️ Future Roadmap
- [ ] Multi-tenant Authentication (JWT + RBAC)
- [ ] Vector Database Integration (RAG) for localized context.
- [ ] Multi-LLM Support (OpenAI, Anthropic).
- [ ] Advanced Anomaly Detection using ML models.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
