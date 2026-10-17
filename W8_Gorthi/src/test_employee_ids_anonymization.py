from pathlib import Path

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine

base_dir = Path(__file__).resolve().parents[1]
input_file = base_dir / "data" / "stress_test" / "pii_adversarial.md"
text = input_file.read_text(encoding="utf-8")

patterns = [
    Pattern(name="emp_id", regex=r"\bEMP-\d{5}\b", score=0.90),
    Pattern(name="staff_id", regex=r"\bStaff\s*#\s*\d{4,}\b", score=0.90),
    Pattern(name="regional_id", regex=r"\bRJP/\d{4}/\d{4}\b", score=0.90),
    Pattern(name="european_id", regex=r"\bA\.M\.-\d{4}-EUR-\d{3}\b", score=0.90),
    Pattern(name="badge_id", regex=r"\bBadge:\s*CM\d{5}\b", score=0.90),
]

recognizer = PatternRecognizer(
    supported_entity="EMPLOYEE_ID",
    patterns=patterns,
)

analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(recognizer)
anonymizer = AnonymizerEngine()

results = analyzer.analyze(
    text=text,
    language="en",
    entities=["EMPLOYEE_ID"],
)

anonymized = anonymizer.anonymize(
    text=text,
    analyzer_results=results,
).text

print("=== EMPLOYEE-ID ANONYMIZATION TEST ===")
print(f"Detected identifiers: {len(results)}")

for identifier in (
    "EMP-04827",
    "Staff #4082",
    "RJP/2019/0451",
    "A.M.-2021-EUR-007",
    "Badge: CM18234",
):
    print(f"{identifier}: {'REDACTED' if identifier not in anonymized else 'STILL PRESENT'}")

print("\n=== ANONYMIZED EXCERPT ===")
start = anonymized.find("## Employee identifiers")
end = anonymized.find("## Addresses")
print(anonymized[start:end])
