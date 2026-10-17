from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class DocumentChunk:
    document_id: str
    chunk_id: str
    source: str
    file_type: str
    section: str
    text: str
    page: Optional[int] = None
    contains_pii: bool = False
    metadata_version: int = 1


def main() -> None:
    chunks = [
        DocumentChunk(
            document_id="POL-001",
            chunk_id="POL-001-001",
            source="company_policies.pdf",
            file_type="pdf",
            section="Leave Approval",
            text="Employees must obtain manager approval before planned leave.",
            page=1,
        ),
        DocumentChunk(
            document_id="POL-001",
            chunk_id="POL-001-002",
            source="company_policies.pdf",
            file_type="pdf",
            section="IT Support",
            text="Contact the IT Support team when company equipment fails.",
            page=1,
        ),
        DocumentChunk(
            document_id="PROD-001",
            chunk_id="PROD-001-001",
            source="product_page.html",
            file_type="html",
            section="Warranty",
            text="The product includes a standard one-year limited warranty.",
        ),
    ]

    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks:
        record = asdict(chunk)
        print("\n--- Chunk record ---")
        print(json.dumps(record, indent=2))

    # Demonstrate metadata filtering.
    warranty_chunks = [
        chunk for chunk in chunks
        if chunk.section == "Warranty"
    ]

    print("\n--- Warranty filter results ---")
    print(f"Matching chunks: {len(warranty_chunks)}")
    for chunk in warranty_chunks:
        print(f"{chunk.source} | {chunk.section} | {chunk.text}")


if __name__ == "__main__":
    main()
