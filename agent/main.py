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

app = FastAPI(title="OpsAgent App", version="1.0", description="")

Base.metadata.create_all(bind=engine)

running = True


async def log_monitor():
    global running
    print("Log monitor started")
    while running:
        print("checking logs...")
        await asyncio.sleep(100)


@app.on_event("startup")
async def startup_event():
    app.state.monitor_task = asyncio.create_task(log_monitor())


@app.on_event("shutdown")
async def shutdown_even():
    global running
    running = False
    await app.state.monitor_task
    print("Log monitor stopped")


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
    return f"quetsion asked is {message}"


@app.get("/alerts")
def server_alerts(
    limit: int = 2, severity: Optional[Level] = None, db: Session = Depends(get_db)
):
    return get_alerts(db, limit=limit, severity=severity)


@app.get("/alerts/{alert_id}")
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    return get_alert(db, alert_id)
