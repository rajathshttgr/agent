from fastapi import FastAPI, HTTPException
import logging
import os
import time
import random

logger = logging.getLogger(__name__)
app = FastAPI(
    title="Demo App", version="1.0", description="A demo app to test agent capabilities"
)

FAKE_API_KEY = "valid_key"
MEMORY_HOG = []

state = {
    "login_attempts": 0,
    "feature_flag": False,
}


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info("Read item endpoint accessed with item_id=%s and q=%s", item_id, q)
    return {"item_id": item_id, "q": q}


@app.get("/memory_leak")
def memory_leak():
    logger.warning("Simulating memory leak")
    MEMORY_HOG.append("X" * 10_000_000)
    return {"status": "memory growing"}


@app.get("/external_api")
def external_api_call(api_key: str):
    logger.info("External API call attempted")
    if api_key != FAKE_API_KEY:
        logger.error("API key expired or invalid")
        raise HTTPException(status_code=401, detail="API key expired")
    return {"status": "success"}


@app.get("/db_query")
def db_query():
    if random.choice([True, False]):
        logger.error("Database connection refused")
        raise HTTPException(status_code=503, detail="DB unavailable")
    return {"data": "fake_db_data"}


@app.post("/login")
def login():
    state["login_attempts"] += 1
    logger.info(f"Login attempt #{state['login_attempts']}")

    if state["login_attempts"] > 3:
        state["feature_flag"] = True
        logger.warning("Feature flag enabled after repeated login attempts")

    return {"message": "login attempted"}


@app.get("/sensitive_action")
def sensitive_action():
    if state["feature_flag"]:
        logger.error("Corrupted state detected - feature flag misused")
        raise HTTPException(status_code=500, detail="State corruption")
    return {"message": "safe"}


@app.post("/zero_division")
def zero_crash():
    logger.error("Forcing ZeroDivisionError")
    return 1 / 0


@app.get("/slow")
def slow():
    logger.warning("Simulating slow response")
    time.sleep(15)
    return {"status": "delayed"}
