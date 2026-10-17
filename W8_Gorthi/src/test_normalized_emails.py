from pathlib import Path
from presidio_analyzer import AnalyzerEngine
from normalize_obfuscated_emails import normalize_obfuscated_emails

base_dir = Path(__file__).resolve().parents[1]
input_file = base_dir / "data" / "stress_test" / "pii_adversarial.md"

original = input_file.read_text(encoding="utf-8")
normalized = normalize_obfuscated_emails(original)

analyzer = AnalyzerEngine()
results = analyzer.analyze(text=normalized, language="en")

print("=== NORMALIZED EMAIL DETECTION ===")

email_results = [
    result for result in results
    if result.entity_type == "EMAIL_ADDRESS"
]

for result in email_results:
    value = normalized[result.start:result.end]
    print(f"Detected: {value} | Score: {result.score:.2f}")

print(f"\nTotal EMAIL_ADDRESS detections: {len(email_results)}")
