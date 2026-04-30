# AI Ops Command | Enterprise Automation Platform ⚡

AI Ops Command is a production-grade AI operations platform designed to automate repetitive business workflows using Large Language Models (LLMs), structured business data, and a distributed microservices architecture.

The platform transforms raw data into strategic intelligence through specialized AI pipelines, providing real-time monitoring, cost analysis, and operational insights.

---

## 🏛️ Architecture

The platform is built on a decoupled, scalable architecture designed for high availability and observability:

- **Frontend**: Streamlit-based Enterprise Dashboard (Command Center).
- **Backend**: FastAPI V1 REST API (Orchestration Layer).
- **Task Queue**: Celery + Redis (Asynchronous Processing).
- **Database**: PostgreSQL 15 (Persistent Execution History).
- **AI Core**: Google Gemini (Structured Reasoning & Analysis).

---

## 🌟 Visual Showcase

### 📊 Operational Intelligence
Real-time tracking of system health, success rates, and performance metrics.
![Strategic Overview](https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION/blob/main/docs/screenshots/overview.png?raw=true)

### 🛒 Workflow Marketplace
Modular AI automation engines for Fraud, Support, KPI, and Document Intelligence.
![Workflow Marketplace](https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION/blob/main/docs/screenshots/marketplace.png?raw=true)

### 🕵️ Audit & Execution Logs
Detailed audit trail for every AI inference, including latency and token consumption.
![Execution Logs](https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION/blob/main/docs/screenshots/logs.png?raw=true)

---

## 🛠️ Specialized AI Workflows

1. **Customer Support Ticket Automation**: 
   - Automated classification, priority detection, and sentiment analysis.
2. **Financial Fraud Risk Analysis**: 
   - Anomaly detection with real-time Slack alerting for high-risk transactions.
3. **Executive KPI Intelligence**: 
   - Strategic summarization of business metrics and management reporting.
4. **Document Intelligence Workflow**: 
   - Automated risk extraction and action item generation from legal/business docs.

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Gemini API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aakashdoli/AI-WORKFLOW-AUTOMATION.git
   cd AI-WORKFLOW-AUTOMATION
   ```

2. **Configure Environment**:
   Create a `.env` file based on `.env.example`:
   ```env
   GEMINI_API_KEY=your_key_here
   DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_ops
   REDIS_URL=redis://redis:6379/0
   ```

3. **Launch the Platform**:
   ```bash
   docker-compose up --build
   ```

4. **Seed Demo Data**:
   ```bash
   docker-compose exec api python backend/scripts/seed_data.py
   ```

**Dashboard Access**: [http://localhost:8501](http://localhost:8501)  
**API Documentation**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## 📈 Future Roadmap
- [ ] JWT-based Multi-tenant Authentication.
- [ ] Multi-provider LLM support (Anthropic/OpenAI).
- [ ] Real-time WebSocket log streaming.
- [ ] Advanced Vector Search (RAG) for Document Intelligence.

---

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
