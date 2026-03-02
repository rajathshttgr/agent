import asyncio
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from agent.tools.container_manager import (
    run_container,
    stop_container,
    remove_container,
)

from sqlalchemy.orm import Session
from agent.config.db import Base, engine, get_db
from agent.config.models import Level
from agent.alerts import get_alerts, get_alert

from agent.config.qdrant_client import init_collections

from agent.log_monitor import LogMonitor, worker

app = FastAPI(title="OpsAgent App", version="1.0", description="")

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():

    app.state.queue = asyncio.Queue()
    app.state.stop_event = asyncio.Event()
    app.state.tasks = []

    await init_collections()

    monitor = LogMonitor(app.state.queue, app.state.stop_event)

    t1 = asyncio.create_task(monitor.start())
    t2 = asyncio.create_task(worker(app.state.queue, app.state.stop_event))

    app.state.tasks.extend([t1, t2])

    print("OpsAgent started.")


@app.on_event("shutdown")
async def shutdown_event():
    print("Stopping OpsAgent...")

    app.state.stop_event.set()

    for task in app.state.tasks:
        task.cancel()

    # wait for cleanup
    await asyncio.gather(*app.state.tasks, return_exceptions=True)

    print("OpsAgent stopped gracefully.")


@app.get("/")
def read_root():
    return {"message": "OpsAgent running..."}


@app.get("/health")
def agent_health():
    return {"messaage": "agent health report will be displayed here"}


@app.post("/stop")
def stop_server():
    try:
        stop_container()
        return {"message": "Container stopped successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to stop container: {str(e)}"
        )


@app.post("/relaunch")
def relaunch_server():
    try:
        stop_container()
        remove_container()
        run_container()
        return {"message": "Container relaunched successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to relaunch container: {str(e)}"
        )


class Question(BaseModel):
    message: str


@app.post("/ask")
def ask_agent(message: Question):
    # you can ask any question related to server health, logs, alerts etc.
    return f"quetsion asked is {message}"


@app.get("/alerts")
def server_alerts(
    limit: int = 2, severity: Optional[Level] = None, db: Session = Depends(get_db)
):
    return get_alerts(db, limit=limit, severity=severity)


@app.get("/alerts/{alert_id}")
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    return get_alert(db, alert_id)
