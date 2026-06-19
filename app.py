import streamlit as st
import os
from google import genai
from google.genai import types

# 1. Page Configuration & Styling
st.set_page_config(page_title="Tech Stack Advisor", page_icon="💻", layout="centered")

st.title("Enterprise Tech Stack Advisor 🚀")
st.markdown("Provide your project vision, scale requirements, or corporate constraints, and get an industry-grade architectural blueprint.")

# 2. Secure API Client Initialization
# Pulls directly from the Hugging Face Settings Secret we injected
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔒 Google API Key not found. Please configure GOOGLE_API_KEY in your environment secrets.")
else:
    client = genai.Client(api_key=api_key)

    # 3. Sidebar Filter Controls for Precise Context Engineering
    st.sidebar.header("🎯 Project Parameters")
    project_type = st.sidebar.selectbox(
        "Application Type",
        ["Web Application", "Mobile App Backend", "Data Engineering / Analytics Pipeline", "Microservices Ecosystem", "IoT / Edge Computing"]
    )
    expected_scale = st.sidebar.selectbox(
        "Expected Scale / Traffic",
        ["Low (Internal Tool / MVP)", "Medium (Up to 100k MAU)", "High (Millions of requests, high concurrency)"]
    )
    primary_cloud = st.sidebar.selectbox(
        "Target Cloud Provider",
        ["Cloud Agnostic / Multi-Cloud", "AWS", "Google Cloud (GCP)", "Microsoft Azure", "On-Premises / Docker Dedicated"]
    )

    # 4. User Inputs
    user_requirements = st.text_area(
        "Describe your project requirements, goals, and business constraints:",
        placeholder="e.g., Building a high-throughput financial transaction processing engine that requires strict ACID compliance, audit logging, and low-latency read operations."
    )

    if st.button("Generate Architectural Blueprint", type="primary"):
        if not user_requirements.strip():
            st.warning("Please provide some project details first!")
        else:
            with st.spinner("Analyzing requirements and engineering system blueprint..."):
                try:
                    # 5. Advanced System Instructions (System Prompting)
                    system_prompt = (
                        "You are a Principal Software Architect and Technology Consultant. Your task is to evaluate project "
                        "requirements and provide a highly technical, production-ready architectural blueprint.\n\n"
                        "Structure your response exactly with these sections:\n"
                        "### 🏗️ Recommended Tech Stack Matrix\n"
                        "Provide a clean breakdown of Language, Framework, Database, Caching, and Infrastructure components.\n"
                        "### 🔬 Architectural Justification\n"
                        "Explain exactly WHY these tools were selected based on the user's constraints, scale requirements, and application type.\n"
                        "### 📉 Trade-offs & Engineering Challenges\n"
                        "Detail the potential downsides of this stack (e.g., operational complexity, eventual consistency issues, or learning curves) and how to mitigate them.\n"
                        "### 🛠️ Next Steps for Implementation\n"
                        "Provide concrete steps to quickly spin up an MVP with this architecture."
                    )

                    # Combined context block
                    full_context = f"Context: Application Type is {project_type}, Target Scale is {expected_scale}, Hosting on {primary_cloud}.\nRequirements: {user_requirements}"

                    # 6. Execute Gemini API Call
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_context,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.2 # Lower temperature forces more analytical, deterministic technical choices
                        )
                    )
                    
                    st.success("✨ Architectural Strategy Generated Successfully!")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"An error occurred while generating the advice: {e}")