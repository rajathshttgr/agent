import uuid
from datetime import datetime, timezone
import asyncio
from agent.config.openai_client import client as openai_client
from agent.config.qdrant_client import client as qdrant_client


COLLECTION_NAME = "incident_memory"


async def embed_text(text: str):
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def build_embedding_text(payload: dict) -> str:
    """
    Create semantically rich text for embedding.
    """
    return f"""
    Incident Title: {payload.get("title")}
    Error Type: {payload.get("error_type")}
    Service: {payload.get("service")}
    Root Cause: {payload.get("root_cause")}
    Resolution: {payload.get("resolution")}
    Prevention: {payload.get("prevention")}
    """


async def store_incident(payload: dict):
    incident_id = str(uuid.uuid4())
    embedding_text = build_embedding_text(payload)

    vector = await embed_text(embedding_text)

    payload["incident_id"] = incident_id
    payload["created_at"] = datetime.now(timezone.utc).isoformat()

    await qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[{"id": incident_id, "vector": vector, "payload": payload}],
    )

    return incident_id


if __name__ == "__main__":
    sample_incident = {
        "title": "Database Connection Timeout",
        "error_type": "TimeoutError",
        "service": "User Service",
        "root_cause": "Network latency causing DB connections to timeout",
        "resolution": "Increased DB connection timeout and optimized queries",
        "prevention": "Implement connection pooling and monitor network latency",
    }
    incident_id = asyncio.run(store_incident(sample_incident))
    print(f"Incident stored with ID: {incident_id}")
