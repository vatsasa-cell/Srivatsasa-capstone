import json
import os
import uuid
from pathlib import Path

from openai import OpenAI
from qdrant_client import QdrantClient, models

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "ingestion_output.json"
COLLECTION = "w8_ingestion_gorthi"
EMBEDDING_MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    if not os.environ.get("QDRANT_URL") or not os.environ.get("QDRANT_API_KEY"):
        raise RuntimeError("QDRANT_URL or QDRANT_API_KEY is not set.")

    chunks = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("Expected a non-empty JSON list of chunks.")

    required = {
        "document_id", "chunk_id", "source", "file_type",
        "section", "text", "page", "contains_pii", "metadata_version",
    }

    for index, chunk in enumerate(chunks):
        missing = required - chunk.keys()
        if missing:
            raise ValueError(f"Chunk {index} is missing fields: {sorted(missing)}")
        if not chunk["text"].strip():
            raise ValueError(f"Chunk {index} has empty text.")
        if chunk["contains_pii"]:
            raise ValueError(
                f"Chunk {chunk['chunk_id']} is flagged for PII. "
                "Review/redact it before uploading."
            )

    qdrant = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
        timeout=30,
        check_compatibility=False,
    )

    try:
        existing = {
            item.name for item in qdrant.get_collections().collections
        }

        if COLLECTION in existing:
            raise RuntimeError(
                f"{COLLECTION} already exists. Nothing was changed; "
                "inspect it before deciding how to proceed."
            )

        # Generate vectors before creating the remote collection.
        openai_client = OpenAI()
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[chunk["text"] for chunk in chunks],
        )

        embeddings = [
            item.embedding for item in sorted(
                response.data, key=lambda item: item.index
            )
        ]

        if len(embeddings) != len(chunks):
            raise RuntimeError("Embedding count does not match chunk count.")

        if any(len(vector) != VECTOR_SIZE for vector in embeddings):
            raise RuntimeError("An embedding has an unexpected vector size.")

        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )

        points = []
        for chunk, vector in zip(chunks, embeddings):
            # Stable point IDs make each chunk identifiable.
            point_id = str(
                uuid.uuid5(uuid.NAMESPACE_URL, chunk["chunk_id"])
            )
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=chunk,
                )
            )

        qdrant.upsert(
            collection_name=COLLECTION,
            points=points,
            wait=True,
        )

        info = qdrant.get_collection(COLLECTION)
        print("Week 8 upload successful.")
        print("Collection:", COLLECTION)
        print("Uploaded chunks:", len(points))
        print("Stored points:", info.points_count)
        print("Status:", info.status)
        print("Vector size:", info.config.params.vectors.size)
        print("Distance:", info.config.params.vectors.distance)

    finally:
        qdrant.close()


if __name__ == "__main__":
    main()
