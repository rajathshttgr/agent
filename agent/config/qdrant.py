from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="incident_memory",
    vectors_config=VectorParams(size=100, distance=Distance.COSINE),
)

client.create_collection(
    collection_name="critical_logs",
    vectors_config=VectorParams(size=100, distance=Distance.COSINE),
)
