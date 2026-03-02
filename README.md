# OpsAgent

Goal-driven autonomous AI agent that monitors service health, diagnoses incidents, and takes bounded recovery actions.

### Key Features

- Goal-driven agent loop (observe → decide → act)
- Dynamic tool selection
- Log intelligence (RAG over logs)
- Severity classification
- Automatic restart (bounded action)
- Slack alert routing
- Incident memory
- Confidence scoring
- Escalation logic
- Docker-based safe execution

### Tech Stack

- FastAPI
- LangChain
- LangGraph
- OpenAI API (LLM)
- Qdrant
- SQLite
- Docker
- Docker Compose
- Slack Webhook

## Get Started

- Build your fastapi app image and configure in `tools/container_manager.py`

### 1. Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI

```bash
uvicorn agent.main:app --reload --port 9000
```

## Quick Hosting

```bash
cloudflared tunnel --url http://localhost:9000
```

## Design Summary

```
START
  ↓
analyze_log (LLM)
  ↓
decision_router
   ↙        ↓         ↘
restart   slack    alerts
   ↓         ↓         ↓
store_incident_memory
   ↓
END
```
