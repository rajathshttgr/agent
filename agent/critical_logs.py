import hashlib
import uuid

from agent.config.openai_client import client as openai_client
from agent.config.qdrant_client import client as qdrant_client

from .agent import graph

COLLECTION_NAME = "critical_logs"
EMBEDDING_MODEL = "text-embedding-3-small"


def normalize_log(text: str) -> str:
    # Remove timestamps for better semantic match
    lines = text.splitlines()
    cleaned = []
    for l in lines:
        parts = l.split("|")
        if len(parts) >= 4:
            cleaned.append(parts[-1].strip())
        else:
            cleaned.append(l)
    return "\n".join(cleaned)


def hash_log(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


async def embed_text(text: str):
    response = await openai_client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


async def process_critical_event(event: str):
    normalized = normalize_log(event)
    error_hash = hash_log(normalized)

    vector = await embed_text(normalized)

    point_id = str(uuid.uuid4())

    await qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": point_id,
                "vector": vector,
                "payload": {
                    "error_hash": error_hash,
                    "raw": event,
                },
            }
        ],
    )

    print("Stored critical log in vector DB")

    print("Calling Ops Agent")
    await graph.ainvoke({"log": event})
