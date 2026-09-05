# Agentic Incident Flow: Automated AI-Driven ServiceNow Management

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logoColor=white" alt="Groq" />
  <img src="https://img.shields.io/badge/ServiceNow-81B5A1?style=for-the-badge&logo=servicenow&logoColor=white" alt="ServiceNow" />
  <img src="https://img.shields.io/badge/ngrok-1F1E37?style=for-the-badge&logo=ngrok&logoColor=white" alt="ngrok" />
</p>

## Overview

A production-ready **Agentic Incident Flow** system designed to automate IT support workflows by bridging ServiceNow incidents with LLM-powered decision making. Leveraging LangChain and the ultra-fast Groq LPU, this service intercepts new ServiceNow tickets via webhooks, intelligently analyzes them against a predefined Knowledge Base, and automatically responds, resolves, or escalates tickets back in ServiceNow.

The system relies on a robust event-driven architecture featuring FastAPI for high-performance webhook routing and asynchronous background processing, ensuring that ServiceNow users experience zero latency when submitting tickets.

## ✨ Key Features

- **Automated Ticket Resolution:** Automatically resolves simple, known issues by mapping them to KB articles and updating the ServiceNow state directly to "Resolved".
- **Intelligent Clarification:** Detects ambiguous tickets and automatically posts a comment asking the user for more specific information.
- **Human-in-the-Loop Escalation:** Escalates unknown or highly complex issues to human agents, appending a detailed reasoning report to the ticket's internal work notes.
- **Ultra-Fast Inference:** Powered by Groq's high-speed inference endpoints to ensure instantaneous incident triage.
- **Robust Webhook Integration:** Uses FastAPI to expose a secure and high-performance endpoint capable of receiving real-time JSON payloads from ServiceNow Business Rules.

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI, Python (>=3.12)
- **AI & LLM Orchestration:** LangChain Core, Groq (Qwen/Llama models)
- **Data Validation:** Pydantic

### Integrations & Tooling
- **External API:** ServiceNow REST API (via `requests` with Basic Auth)
- **Environment Management:** `uv` (Extremely fast Python package and project manager)
- **Tunneling:** `ngrok` (Secure introspectable tunnels to localhost)

## 📁 Project Structure

```text
agentic-incident-flow/
├── ai_service.py         # LangChain logic, prompts, and Groq LLM configuration
├── main.py               # FastAPI server, webhook routes, and background tasks
├── models.py             # Pydantic schemas for ServiceNow JSON payloads
├── servicenow_client.py  # HTTP client for patching ServiceNow incidents
├── Knowledge_Base/       # Files defining standard operating procedures (SOPs)
├── .env.example          # Template for required environment variables
└── README.md
```

## 🏃‍♂️ Getting Started

Anyone can clone this repository, follow these steps, and run the service locally.

1. **Clone & Initialize Project:**
   ```bash
   git clone https://github.com/Mo0Hanned/Automated-AI-Driven-ServiceNow-Management.git
   cd Agentic_Incident_Flow
   ```

2. **Setup Virtual Environment & Install Dependencies:**
   ```bash
   uv venv --python 3.12
   source .venv/bin/activate
   uv sync
   ```

3. **Configure Environment Variables:**
   Copy the example environment file and fill in your actual details:
   ```bash
   cp .env.example .env
   ```
   *(Ensure you provide your `GROQ_API_KEY`, `SN_INSTANCE_URL`, `SN_USERNAME`, and `SN_PASSWORD` in the `.env` file).*

4. **Run the Backend (FastAPI):**
   ```bash
   uvicorn main:app --reload
   ```

5. **Expose the Webhook with ngrok (In a separate terminal):**
   ```bash
   ngrok http 8000
   ```
   *Copy the Forwarding URL provided by ngrok (e.g., `https://<id>.ngrok-free.app`) and configure your ServiceNow Business Rule to send POST requests to `https://<id>.ngrok-free.app/webhook`.*

## 🧠 Architecture & Design Choices

The system is built on a streamlined, event-driven architecture designed to operate asynchronously without blocking ServiceNow's interface.

- **Background Task Processing:** Webhooks from ServiceNow are immediately acknowledged (HTTP 202 Accepted) by FastAPI. The actual LLM reasoning and ServiceNow API HTTP PATCH updates are offloaded and processed via FastAPI `BackgroundTasks`. This prevents webhook timeouts on the ServiceNow side.
- **Structured LLM Output:** We enforce strict Pydantic structures (`with_structured_output`) on the Groq model. This restricts the LLM from hallucinating conversational text and ensures the agent consistently outputs a machine-readable `decision` and `message`.
- **Secure Integration Practices:** We communicate back to ServiceNow using dedicated Integration Users with the `snc_basic_auth_api_access` role, adhering to modern strict API Access Policies.

## 🚀 Future Work

As the project evolves, the next major phase focuses on scaling the knowledge retrieval and introducing complex routing.

- **Vector Database Integration (RAG):** 
  - Migrate the static, hardcoded Knowledge Base to a scalable vector store (e.g., Qdrant or Milvus) to support semantic search across thousands of IT SOPs and historic resolved tickets.
- **Multi-Agent Triage (LangGraph):** 
  - Implement LangGraph to route tickets to specialized sub-agents (e.g., Network Agent, Hardware Agent, Software Agent) based on initial classification, allowing for more nuanced troubleshooting steps.
- **Cloud Deployment & CI/CD:** 
  - Containerize the application with Docker.
  - Implement GitHub Actions to automate deployment to AWS ECS or Google Cloud Run for high availability and load balancing.
