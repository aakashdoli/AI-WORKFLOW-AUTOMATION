import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.database_service import DatabaseService, init_db
from app.services.llm_service import LLMService
from app.pipelines.reporting_pipeline import ReportingPipeline

# Page Config
st.set_page_config(page_title="AI Workflow Automation Platform", layout="wide", page_icon="🤖")

# Initialize DB
init_db()

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .report-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("AI Ops Dashboard")
menu = st.sidebar.radio("Navigation", ["Workflow Overview", "Execute Pipeline", "Execution History"])

# Services
db_service = DatabaseService()
try:
    llm_service = LLMService()
except Exception as e:
    st.sidebar.error(f"LLM Service Error: {e}")
    llm_service = None

if menu == "Workflow Overview":
    st.title("📈 Workflow Operational Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    workflows = db_service.get_all_workflows()
    executions = db_service.get_executions()
    
    with col1:
        st.metric("Total Workflows", len(workflows))
    with col2:
        st.metric("Total Executions", len(executions))
    with col3:
        completed = [e for e in executions if e.status == "COMPLETED"]
        st.metric("Success Rate", f"{len(completed)/len(executions)*100:.1f}%" if executions else "0%")

    st.subheader("Recent Activity")
    if executions:
        exec_df = pd.DataFrame([{
            "ID": e.id,
            "Workflow": e.workflow.name,
            "Status": e.status,
            "Started At": e.started_at,
            "Duration": (e.completed_at - e.started_at).total_seconds() if e.completed_at else "N/A"
        } for e in executions[:10]])
        st.table(exec_df)
    else:
        st.info("No executions recorded yet.")

elif menu == "Execute Pipeline":
    st.title("🚀 Run Automation Pipeline")
    
    st.markdown("### Upload Business Data (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    workflow_name = st.text_input("Workflow Name", "Ticket Classification Support")
    
    if uploaded_file and st.button("Start AI Pipeline"):
        if not llm_service:
            st.error("Cannot run pipeline: GEMINI_API_KEY is missing.")
        else:
            with st.spinner("🤖 AI is processing your data..."):
                # Save uploaded file temporarily
                temp_path = f"data/outputs/temp_{datetime.now().timestamp()}.csv"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                pipeline = ReportingPipeline(db_service, llm_service)
                try:
                    exec_id, summary = pipeline.run_workflow(workflow_name, temp_path)
                    st.success(f"Pipeline executed successfully! Execution ID: {exec_id}")
                    
                    st.markdown("### Executive Summary")
                    st.markdown(summary)
                    
                    # Clean up
                    os.remove(temp_path)
                except Exception as e:
                    st.error(f"Pipeline failed: {e}")

elif menu == "Execution History":
    st.title("📜 Execution History & Results")
    
    executions = db_service.get_executions()
    if executions:
        exec_ids = [f"Execution #{e.id} - {e.workflow.name} ({e.status})" for e in executions]
        selected_exec_str = st.selectbox("Select Execution to View Results", exec_ids)
        selected_id = int(selected_exec_str.split("#")[1].split(" ")[0])
        
        results = db_service.get_results(selected_id)
        
        if results:
            st.subheader("Classification Results")
            # Filter out the executive summary from the results table
            class_results = [r for r in results if r.category != "Executive Summary"]
            exec_summary = next((r for r in results if r.category == "Executive Summary"), None)
            
            if class_results:
                res_df = pd.DataFrame([{
                    "Category": r.category,
                    "Priority": r.priority,
                    "Input Data": r.input_data,
                    "AI Reasoning": r.output_data
                } for r in class_results])
                st.dataframe(res_df, use_container_width=True)
            
            if exec_summary:
                st.subheader("Generated Executive Summary")
                st.markdown(exec_summary.output_data)
        else:
            st.info("No results found for this execution.")
    else:
        st.info("No executions recorded yet.")

db_service.close()
