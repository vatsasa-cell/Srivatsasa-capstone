import json
from dataclasses import asdict, dataclass
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

@dataclass
class DocumentChunk:
    document_id: str
    chunk_id: str
    source: str
    file_type: str
    section: str
    text: str
    page: int | None = None
    contains_pii: bool = False
    metadata_version: int = 1

raw_text = """Employee contact:
Name: Alice Example
Email: alice.example@example.com
Phone: +1-202-555-0147

The employee must obtain manager approval before planned leave.
"""

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Detect PII in the original text.
results = analyzer.analyze(text=raw_text, language="en")

# Redact detected entities before creating the chunk.
redacted_text = anonymizer.anonymize(
    text=raw_text,
    analyzer_results=results
).text

# contains_pii records whether PII was detected in the original text.
chunk = DocumentChunk(
    document_id="hr-policy-001",
    chunk_id="hr-policy-001-chunk-001",
    source="sample_hr_policy.txt",
    file_type="txt",
    section="Employee Contact",
    text=redacted_text,
    page=None,
    contains_pii=bool(results)
)

print("=== Redacted Chunk Text ===")
print(chunk.text)

print("\\n=== Chunk Metadata ===")
print(json.dumps(asdict(chunk), indent=2))

print("\\n=== Validation ===")
print("PII detected in original:", bool(results))
print("Original email remains in chunk:", "alice.example@example.com" in chunk.text)
print("Original phone remains in chunk:", "+1-202-555-0147" in chunk.text)
print("Original name remains in chunk:", "Alice Example" in chunk.text)
