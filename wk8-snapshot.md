# Week 8 Snapshot — Document Ingestion, Metadata and PII

## Completed exercises

- Parsed PDF, DOCX and HTML sample documents.
- Compared PyMuPDF and pdfplumber extraction.
- Tested OCR fallback on a scanned PDF.
- Practiced fixed-size, recursive, semantic and structure-aware chunking.
- Added metadata fields and tested metadata filtering.
- Practiced regex-based PII detection and redaction.
- Ran Presidio analysis and anonymization examples.
- Built and ran a sample document-ingestion pipeline.
- Created Week 8 Qdrant collection `w8_ingestion_gorthi` with five points.
- Tested metadata-filtered retrieval.

## PII stress-test progress

- Created adversarial corpus at
  `W8_Gorthi/data/stress_test/pii_adversarial.md`.
- Baseline Presidio run: 43 detections across 1,619 characters.
- Email normalization: 3 of 3 obfuscated email examples detected after normalization.
- Employee-ID regex test: 5 of 5 expected formats matched.
- Presidio employee-ID test: 5 of 5 identifiers detected.
- Employee-ID anonymization test: 5 of 5 identifiers replaced in the test output.
- Findings recorded in `docs/adr/pii_stress_test_findings.md`.

## Limitations and follow-up

- The PII results use a synthetic test corpus and do not establish production readiness.
- Email normalization and the custom employee-ID recognizer have not been integrated into the main ingestion pipeline.
- Phone-number normalization, address coverage, masked-card detection and false-positive review remain potential improvements.
- The stress-test corpus has not been uploaded to Qdrant.
- The Week 7 collection and files remain separate and unchanged.
