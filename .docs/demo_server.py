from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", mode="a"),  # append-only
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error at {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}


@app.post("/zero_crash")
def divide_by_zero():
    logger.info("Attempting division by zero")
    return 1 / 0


@app.post("/hard_crash")
def hard_crash():
    os._exit(1)  # Immediate process termination


big_data = []


@app.post("/memory_leak")
def memory_leak():
    global big_data
    while True:
        big_data.append("A" * 10_000_000)


## version 2

from fastapi import FastAPI
import logging

# Get module-level logger
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info("Read item endpoint accessed with item_id=%s and q=%s", item_id, q)
    return {"item_id": item_id, "q": q}


@app.post("/zero_division")
def divide_by_zero():
    logger.info("Attempting division by zero")
    return 1 / 0
