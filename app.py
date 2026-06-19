import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Page Configuration & Professional Styling
st.set_page_config(
    page_title="AI Architecture Consultant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom dark-mode friendly CSS tweaks
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stDeployButton { display:none; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Advanced AI & Systems Architecture Advisor")
st.markdown("---")

# 2. Secure API Client Initialization via LangChain Environment Setup
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🔒 Security Key Error: GOOGLE_API_KEY environment variable missing from Cloud Provider Secrets.")
    st.stop()

# Initialize the modern LangChain Gemini LLM wrapper
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.15  # Low temperature forces predictable, analytical, industry-standard engineering patterns
)

# 3. Sidebar Structural Parameters for Advanced Context Engineering
st.sidebar.header("⚙️ System Boundaries")
app_paradigm = st.sidebar.selectbox(
    "AI Architecture Core",
    [
        "Retrieval-Augmented Generation (RAG / Agentic)",
        "Edge AI & On-Device Local Inference",
        "Distributed Computing & Federated Learning",
        "Privacy-Preserving Data Analytics"
    ]
)

scale_tier = st.sidebar.selectbox(
    "Target Scale / Workload",
    [
        "MVP / Academic Evaluation Proof-of-Concept",
        "Medium Scale (Localized Cluster / Cloud Instances)",
        "High Scale Enterprise (Massive Data Streams / High Concurrency)"
    ]
)

privacy_level = st.sidebar.selectbox(
    "Privacy Guardrail Constraints",
    [
        "Strict Local Privacy (Zero-Trust Third Party Cloud)",
        "Differential Privacy / Data Minimization Required",
        "Standard Encryption (TLS / Rest / Secret Enclaves)",
        "Not Constrained / Open Public Domain Data"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro-Tip**: Outline your exact data sources, persistence goals, and language preferences on the right.")

# 4. User System Requirements Input
user_prompt = st.text_area(
    "✏️ Enter your System Design Objectives, Research Questions, or Technical Constraints:",
    height=250,
    placeholder="e.g., Designing an isolated, data-driven Learning Analytics ecosystem for higher education institutions. Requires tracking student telemetry without sending raw data to external servers, using localized vector embeddings, and maintaining a strict PostgreSQL system datastore..."
)

# 5. Core Execution Engine (LangChain Expression Language Pipeline)
if st.button("Compile Architectural Strategy Blueprint", type="primary"):
    if not user_prompt.strip():
        st.warning("Please input project parameters or technical specifications before compiling.")
    else:
        with st.spinner("Analyzing structural constraints via LangChain pipeline..."):
            try:
                # Rigorous engineering system template targeting your exact constraints
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", (
                        "You are a Principal Enterprise Solutions Architect and Technical Consultant specializing in advanced AI systems, "
                        "distributed computing, and privacy-preserving machine learning frameworks.\n\n"
                        "Your objective is to provide elite-tier architectural blueprints matching exact user constraints. "
                        "You possess deep technical fluency in Java/Spring Boot ecosystems, Node.js microservice pipelines, Docker multi-container setups, "
                        "PostgreSQL vector extensions (pgvector), specialized indexing, LLMOps pipelines, Edge computing topologies, Federated Learning architectures, "
                        "and Differential Privacy constraints.\n\n"
                        "Structure your output strictly using these Markdown sections:\n"
                        "### 🏗️ Recommended Tech Stack & System Matrix\n"
                        "Provide a precise, readable breakdown of: Languages, Frameworks, Model Runtimes, Database/Vector layers, Caching mechanisms, and Virtualization tools.\n\n"
                        "### 🔬 Detailed AI Pipeline & Data Orchestration Flow\n"
                        "Outline the ingestion, transformation, secure vectorization/embedding steps, model orchestration, and final inference loops.\n\n"
                        "### 🔒 Privacy-Preserving Framework & Security Strategy\n"
                        "Clearly detail the technical mitigations satisfying the privacy constraint tier selected (e.g., exact local isolation patterns, noise injection parameters, decentralized state orchestration, or cryptographic anonymization layers).\n\n"
                        "### 📉 Architectural Trade-offs & Engineering Complexities\n"
                        "Provide an objective technical reality check: discuss latency overheads, cold starts, state synchronization bottlenecks, storage penalties, and exact remediation workflows.\n\n"
                        "### 🛠️ Step-by-Step MVP Implementation Execution Path\n"
                        "Provide an explicit blueprint detailing how to quickly structure files, manage environmental boundaries, and verify system paths locally or via secure Docker container configurations."
                    )),
                    ("human", (
                        "System Constraint Architecture Matrix:\n"
                        "- Core Focus Paradigm: {paradigm}\n"
                        "- Expected Traffic/Workload Scale: {scale}\n"
                        "- Enforced Privacy Boundary: {privacy}\n\n"
                        "User Functional Requirements and System Specifications:\n{requirements}"
                    ))
                ])

                # Build and invoke the LangChain pipeline chain
                chain = prompt_template | llm | StrOutputParser()

                blueprint_output = chain.invoke({
                    "paradigm": app_paradigm,
                    "scale": scale_tier,
                    "privacy": privacy_level,
                    "requirements": user_prompt
                })

                st.success("✨ Architectural Strategy Successfully Compiled!")
                st.markdown(blueprint_output)

            except Exception as e:
                st.error(f"An exception occurred inside the LangChain execution loop: {e}")