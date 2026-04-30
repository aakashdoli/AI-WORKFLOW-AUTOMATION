import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.database_service import DatabaseService, init_db
from app.services.llm_service import LLMService
from app.pipelines.reporting_pipeline import ReportingPipeline

# Page Config
st.set_page_config(page_title="AI Ops | Workflow Automation", layout="wide", page_icon="⚡")

# Initialize DB
init_db()

# Custom CSS for Professional Dark/Light Hybrid Look
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #1E88E5;
    }
    .main-header {
        font-size: 42px;
        font-weight: 800;
        color: #1A237E;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 18px;
        color: #546E7A;
        margin-bottom: 30px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Services
db_service = DatabaseService()
try:
    llm_service = LLMService()
except Exception as e:
    st.sidebar.error(f"LLM Service Error: {e}")
    llm_service = None

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
st.sidebar.title("AI Ops Command")
menu = st.sidebar.selectbox("Navigate", ["Strategic Overview", "Workflow Execution", "Operation logs", "Analytics Deep Dive", "AI System Insights"])

if menu == "Strategic Overview":
# ... (rest of the code remains same)
    st.markdown('<p class="main-header">AI Operations Platform</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time automation monitoring & intelligence</p>', unsafe_allow_html=True)
    
    executions = db_service.get_executions()
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Automations", len(executions))
    with col2:
        success_rate = len([e for e in executions if e.status == "COMPLETED"]) / len(executions) * 100 if executions else 0
        st.metric("Success Rate", f"{success_rate:.1f}%", delta="0.5%")
    with col3:
        avg_latency = sum([e.latency_ms for e in executions if e.latency_ms]) / len(executions) if executions else 0
        st.metric("Avg Latency", f"{avg_latency:.0f}ms", delta="-12ms")
    with col4:
        total_tokens = sum([e.token_usage for e in executions if e.token_usage]) if executions else 0
        st.metric("AI Tokens Used", f"{total_tokens:,}")

    # Charts Row
    c1, c2 = st.columns(2)
    
    if executions:
        df_exec = pd.DataFrame([{
            "Workflow": e.workflow.name,
            "Latency": e.latency_ms or 0,
            "Tokens": e.token_usage or 0,
            "Status": e.status,
            "Date": e.started_at
        } for e in executions])

        with c1:
            st.subheader("Workflow Execution Volume")
            fig = px.pie(df_exec, names='Workflow', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Latency Trends (ms)")
            fig = px.area(df_exec.sort_values("Date"), x="Date", y="Latency", line_shape='spline')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start your first workflow to see analytics.")

elif menu == "Workflow Execution":
    st.title("🚀 Execute Production Pipelines")
    
    workflow_type = st.selectbox("Select Workflow Template", [
        "Customer Support Ticket Classification",
        "Financial Fraud Risk Analysis",
        "Executive KPI Reporting"
    ])
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Batch Data (CSV)", type="csv")
    
    if uploaded_file and st.button("Trigger AI Engine"):
        if not llm_service:
            st.error("AI Service not available. Check API Key.")
        else:
                import requests
                
                payload = {
                    "workflow_name": workflow_type,
                    "csv_path": os.path.abspath(temp_path)
                }
                
                try:
                    # Use internal docker network name 'api' for backend communication
                    backend_url = os.getenv("BACKEND_URL", "http://api:8000")
                    response = requests.post(f"{backend_url}/workflows/execute", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Intelligence gathering triggered! (Task ID: {data['message'].split(': ')[1]})")
                        st.toast("Worker has accepted the payload.")
                    else:
                        st.error(f"Backend Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to AI Engine: {e}")

elif menu == "Operation logs":
    st.title("📜 System Execution Logs")
    
    executions = db_service.get_executions()
    if executions:
        for e in executions[:15]:
            with st.expander(f"#{e.id} | {e.workflow.name} | {e.status} | {e.started_at.strftime('%H:%M:%S')}"):
                st.write(f"**Latency:** {e.latency_ms}ms")
                st.write(f"**Tokens:** {e.token_usage}")
                results = db_service.get_results(e.id)
                if results:
                    st.table(pd.DataFrame([{
                        "Category": r.category,
                        "Priority": r.priority,
                        "Confidence": f"{r.confidence_score}%" if r.confidence_score else "N/A"
                    } for r in results]))
                if e.error_message:
                    st.error(f"Error: {e.error_message}")
    else:
        st.info("No logs available.")

elif menu == "Analytics Deep Dive":
    st.title("🔬 Advanced AI Analytics")
    executions = db_service.get_executions()
    if executions:
        df = pd.DataFrame([{
            "Workflow": e.workflow.name,
            "Latency": e.latency_ms or 0,
            "Tokens": e.token_usage or 0,
            "Status": e.status,
            "Priority": r.priority if (r := next(iter(db_service.get_results(e.id)), None)) else "None"
        } for e in executions])
        
        st.subheader("Tokens vs Latency by Workflow")
        fig = px.scatter(df, x="Tokens", y="Latency", color="Workflow", size="Tokens", hover_data=['Status'])
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Priority Distribution")
        fig = px.histogram(df, x="Priority", color="Workflow", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "AI System Insights":
    st.title("🧠 AI Operational Intelligence")
    st.markdown("Automated system analysis and optimization recommendations.")
    
    from app.pipelines.insights_pipeline import InsightsPipeline
    
    executions = db_service.get_executions()
    if executions and st.button("Generate Intelligence Report"):
        with st.spinner("Analyzing system patterns..."):
            history = [{
                "workflow": e.workflow.name,
                "latency": e.latency_ms,
                "tokens": e.token_usage,
                "status": e.status
            } for e in executions[:50]]
            
            pipeline = InsightsPipeline(llm_service)
            insights = pipeline.generate_system_insights(history)
            
            for insight in insights:
                color = "#FFD700" if insight.impact_level == "Medium" else "#FF4B4B" if insight.impact_level == "High" else "#90EE90"
                st.markdown(f"""
                <div style="padding:15px; border-radius:10px; border-left: 5px solid {color}; background-color:white; margin-bottom:10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="margin:0;">{insight.category}: {insight.finding}</h4>
                    <p style="margin:5px 0;"><b>Recommendation:</b> {insight.recommendation}</p>
                    <span style="background-color:{color}; padding:2px 8px; border-radius:5px; font-size:12px; color:white;">{insight.impact_level} Impact</span>
                </div>
                """, unsafe_allow_html=True)
    elif not executions:
        st.info("Insufficient data for intelligence analysis.")

db_service.close()
