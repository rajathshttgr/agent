# Demo App

## Local Setup

### 1. Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows PowerShell
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

## Docker Setup

### To build docker image

```bash
docker build -t demo-app .

# Optional: Add version tag
docker build -t demo-app:v1 .
```

### To run docker container

```bash
docker run -d -p 8000:8000 --name demo-container demo-app:latest

# with log persistence
docker run -d -p 8000:8000 --name demo-container -e LOG_DIR=/app/logs -v $(pwd)/logs:/app/logs demo-app:latest
```

### To view logs

```bash
docker logs -f demo-container
```

## Expected Errors

| Endpoint            | Type                | Severity | Restart Fix? | Description                            |
| ------------------- | ------------------- | -------- | ------------ | -------------------------------------- |
| `/`                 | Normal              | None     | N/A          | Health check                           |
| `/items/{item_id}`  | Normal              | None     | N/A          | Health check                           |
| `/memory_leak`      | Resource exhaustion | Medium   | Yes          | Gradual memory increase leading to OOM |
| `/external_api`     | Auth failure        | High     | No           | Fails when API key invalid             |
| `/db_query`         | Dependency failure  | Medium   | Sometimes    | Simulates intermittent DB outage       |
| `/login`            | State mutation      | Low      | N/A          | Triggers chain event                   |
| `/sensitive_action` | State corruption    | High     | No           | Fails after multiple login attempts    |
| `/zero_division`    | Logic crash         | High     | No           | Immediate server error                 |
| `/slow`             | Timeout             | Medium   | No           | Simulates long processing delay        |
