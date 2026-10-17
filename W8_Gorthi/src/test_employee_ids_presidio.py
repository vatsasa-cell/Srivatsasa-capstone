from pathlib import Path

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer

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

results = analyzer.analyze(
    text=text,
    language="en",
    entities=["EMPLOYEE_ID"],
)

print("=== PRESIDIO EMPLOYEE-ID TEST ===")
for result in sorted(results, key=lambda item: item.start):
    value = text[result.start:result.end]
    print(f"Detected: {value} | Entity: {result.entity_type} | Score: {result.score:.2f}")

print(f"\nTotal employee IDs detected: {len(results)}/5")
