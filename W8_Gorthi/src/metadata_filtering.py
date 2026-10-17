import json
from pathlib import Path

input_path = (
    Path(__file__).parent.parent
    / "data"
    / "ingestion_output.json"
)
chunks = json.loads(input_path.read_text(encoding="utf-8"))


def show_results(label, results):
    print(f"\n=== {label} ===")
    print(f"Matching chunks: {len(results)}")

    for chunk in results:
        source = chunk["source"]
        section = chunk["section"]
        text = chunk["text"]

        print(f"Source: {source} | Section: {section}")
        print(f"Text: {text}")


# Filter 1: Find the HTML warranty section.
warranty_chunks = [
    c for c in chunks
    if c["file_type"] == "html"
    and c["section"] == "Warranty"
]
show_results("HTML Warranty", warranty_chunks)

# Filter 2: Find chunks from the PDF policy document.
policy_chunks = [
    c for c in chunks
    if c["source"] == "company_policies.pdf"
]
show_results("Company Policies PDF", policy_chunks)

# Filter 3: Find chunks flagged for PII.
pii_chunks = [
    c for c in chunks
    if c["contains_pii"]
]
show_results("Chunks Flagged for PII", pii_chunks)
