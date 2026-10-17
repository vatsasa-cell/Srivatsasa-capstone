import re


SAMPLE_TEXT = """
Employee contact:
Name: Alice Example
Email: alice.example@example.com
Phone: +1-202-555-0147

The employee must obtain manager approval before planned leave.
"""


PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "phone": re.compile(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"
    ),
}


def detect_pii(text: str) -> dict[str, list[str]]:
    findings = {}

    for pii_type, pattern in PATTERNS.items():
        findings[pii_type] = pattern.findall(text)

    return findings


def redact_pii(text: str) -> str:
    redacted = text

    for pii_type, pattern in PATTERNS.items():
        redacted = pattern.sub(
            f"[REDACTED_{pii_type.upper()}]",
            redacted,
        )

    return redacted


def main() -> None:
    findings = detect_pii(SAMPLE_TEXT)

    print("--- Detection results ---")
    for pii_type, matches in findings.items():
        print(f"{pii_type}: {len(matches)} match(es)")

    redacted_text = redact_pii(SAMPLE_TEXT)

    print("\n--- Redacted text ---")
    print(redacted_text)

    print("--- Validation ---")
    print(
        "Original email remains:",
        bool(PATTERNS["email"].search(redacted_text)),
    )
    print(
        "Original phone remains:",
        bool(PATTERNS["phone"].search(redacted_text)),
    )


if __name__ == "__main__":
    main()
