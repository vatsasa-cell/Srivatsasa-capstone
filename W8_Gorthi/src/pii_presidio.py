from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = """Employee contact:
Name: Alice Example
Email: alice.example@example.com
Phone: +1-202-555-0147

The employee must obtain manager approval before planned leave.
"""

results = analyzer.analyze(text=text, language="en")

print("=== Detected PII ===")
for result in results:
    detected_value = text[result.start:result.end]
    print(f"Entity: {result.entity_type}, Value: {detected_value}, Score: {result.score:.2f}")

anonymized_result = anonymizer.anonymize(
    text=text,
    analyzer_results=results
)

print("\n=== Anonymized Text ===")
print(anonymized_result.text)
