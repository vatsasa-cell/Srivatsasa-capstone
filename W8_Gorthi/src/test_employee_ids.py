import re
from pathlib import Path

base_dir = Path(__file__).resolve().parents[1]
input_file = base_dir / "data" / "stress_test" / "pii_adversarial.md"
text = input_file.read_text(encoding="utf-8")

patterns = {
    "EMP_ID": r"\bEMP-\d{5}\b",
    "STAFF_ID": r"\bStaff\s*#\s*\d{4,}\b",
    "REGIONAL_ID": r"\bRJP/\d{4}/\d{4}\b",
    "EUROPEAN_ID": r"\bA\.M\.-\d{4}-EUR-\d{3}\b",
    "BADGE_ID": r"\bBadge:\s*CM\d{5}\b",
}

print("=== EMPLOYEE ID STRESS TEST ===")
total = 0

for label, pattern in patterns.items():
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
    print(f"\n{label}: {len(matches)} match(es)")
    for match in matches:
        print(f"  {match.group(0)}")
    total += len(matches)

print(f"\nTotal identifier matches: {total}/5 expected formats")
