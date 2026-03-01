from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

client = AsyncQdrantClient(host="localhost", port=6333)


async def init_collections():
    if not await client.collection_exists("incident_memory"):
        await client.create_collection(
            collection_name="incident_memory",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    if not await client.collection_exists("critical_logs"):
        await client.create_collection(
            collection_name="critical_logs",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    print("collections initialized successfully")
