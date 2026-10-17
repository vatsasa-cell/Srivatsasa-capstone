from pathlib import Path
from presidio_analyzer import AnalyzerEngine

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "stress_test" / "pii_adversarial.md"

text = INPUT_FILE.read_text(encoding="utf-8")
analyzer = AnalyzerEngine()

results = analyzer.analyze(
    text=text,
    language="en",
)

print("=== PII STRESS TEST: PRESIDIO BASELINE ===")
print(f"Input file: {INPUT_FILE}")
print(f"Characters analyzed: {len(text)}")
print(f"Detections: {len(results)}")

print("\n=== DETECTED VALUES ===")
for result in sorted(results, key=lambda item: item.start):
    value = text[result.start:result.end]
    print(
        f"Entity: {result.entity_type:<20} "
        f"Score: {result.score:.2f}  "
        f"Value: {value!r}"
    )
