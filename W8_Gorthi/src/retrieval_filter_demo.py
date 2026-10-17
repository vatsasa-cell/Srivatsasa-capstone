import json
from pathlib import Path

DATA_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "ingestion_output.json"
)

chunks = json.loads(DATA_PATH.read_text(encoding="utf-8"))


def retrieve_by_metadata(section: str, file_type: str) -> list[dict]:
    """Return chunks matching both metadata conditions."""
    return [
        chunk for chunk in chunks
        if chunk["section"].lower() == section.lower()
        and chunk["file_type"].lower() == file_type.lower()
    ]


def main() -> None:
    section = "Warranty"
    file_type = "html"

    results = retrieve_by_metadata(section, file_type)

    print("=== Metadata-Filtered Retrieval ===")
    print(f"Filter: section={section}, file_type={file_type}")
    print(f"Matching chunks: {len(results)}")

    for chunk in results:
        print(f"\nChunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source']}")
        print(f"Text: {chunk['text']}")


if __name__ == "__main__":
    main()
