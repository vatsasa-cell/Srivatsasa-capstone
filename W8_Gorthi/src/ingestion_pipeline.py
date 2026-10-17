import json
from dataclasses import asdict, dataclass
from pathlib import Path

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from parse_documents import parse_html, parse_docx
from parse_pdf import extract_with_pymupdf
from chunking_structure_aware import structure_aware_html_chunks

BASE_DIR = Path(__file__).parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample_docs"


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


def split_text(text: str, max_chars: int = 500) -> list[str]:
    """Split text at paragraph boundaries where possible."""
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(paragraph), max_chars):
                chunks.append(paragraph[start:start + max_chars])
        elif not current:
            current = paragraph
        elif len(current) + 1 + len(paragraph) <= max_chars:
            current += "\n" + paragraph
        else:
            chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def main() -> None:
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    chunks: list[DocumentChunk] = []

    # 1. Parse PDF, preserving page numbers.
    pdf_path = SAMPLE_DIR / "company_policies.pdf"
    pdf_pages = extract_with_pymupdf(pdf_path)

    for page_number, page_text in enumerate(pdf_pages, start=1):
        for index, text in enumerate(split_text(page_text), start=1):
            chunks.append(DocumentChunk(
                document_id="company-policies",
                chunk_id=f"company-policies-p{page_number}-c{index}",
                source=pdf_path.name,
                file_type="pdf",
                section="Policy",
                text=text,
                page=page_number,
            ))

    # 2. Parse HTML and preserve heading-based sections.
    html_path = SAMPLE_DIR / "product_page.html"
    html_text = parse_html(html_path)

    # Use the existing structure-aware chunker for this sample HTML.
    html_sections = structure_aware_html_chunks()
    if not html_sections and html_text.strip():
        html_sections = [
            {"section": "Document", "text": part}
            for part in split_text(html_text)
        ]

    for index, item in enumerate(html_sections, start=1):
        chunks.append(DocumentChunk(
            document_id="product-page",
            chunk_id=f"product-page-c{index}",
            source=html_path.name,
            file_type="html",
            section=item["section"],
            text=item["text"],
        ))

    # 3. Parse DOCX and split into manageable chunks.
    docx_path = SAMPLE_DIR / "onboarding.docx"
    docx_text = parse_docx(docx_path)

    for index, text in enumerate(split_text(docx_text), start=1):
        chunks.append(DocumentChunk(
            document_id="employee-onboarding",
            chunk_id=f"employee-onboarding-c{index}",
            source=docx_path.name,
            file_type="docx",
            section="Document",
            text=text,
        ))

    # 4. Detect PII and redact before producing the output.
    safe_chunks = []
    for chunk in chunks:
        original_text = chunk.text
        findings = analyzer.analyze(text=original_text, language="en")

        # Narrow exception for this synthetic warranty sample only.
        # Do not suppress DATE_TIME detections globally.
        reviewed_findings = [
            finding for finding in findings
            if not (
                finding.entity_type == "DATE_TIME"
                and original_text[finding.start:finding.end].lower() == "one-year"
                and "warranty" in original_text.lower()
            )
        ]

        redacted_text = anonymizer.anonymize(
            text=original_text,
            analyzer_results=reviewed_findings,
        ).text

        chunk.text = redacted_text
        chunk.contains_pii = bool(reviewed_findings)
        safe_chunks.append(chunk)

    # 5. Print a summary and metadata for inspection.
    output_path = BASE_DIR / "data" / "ingestion_output.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(chunk) for chunk in safe_chunks], indent=2),
        encoding="utf-8",
    )

    print("=== Ingestion Summary ===")
    print(f"Documents processed: 3")
    print(f"Chunks created: {len(safe_chunks)}")
    print(f"Chunks with detected PII: "
          f"{sum(chunk.contains_pii for chunk in safe_chunks)}")
    print(f"Output file: {output_path}")

    print("\n=== Chunk Preview ===")
    for chunk in safe_chunks[:5]:
        print(json.dumps(asdict(chunk), indent=2))


if __name__ == "__main__":
    main()
