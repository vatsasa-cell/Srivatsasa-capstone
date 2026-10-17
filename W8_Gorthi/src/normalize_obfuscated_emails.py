import re

def normalize_obfuscated_emails(text: str) -> str:
    """Normalize common obfuscated email formats for PII analysis."""

    text = text.replace("＠", "@").replace("．", ".")

    text = re.sub(
        r"\s*[\[(]\s*at\s*[\])]\s*",
        "@",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\s*[\[(]\s*dot\s*[\])]\s*",
        ".",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(r"\s+\[\s*at\s*\]\s+", "@", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+\[\s*dot\s*\]\s+", ".", text, flags=re.IGNORECASE)

    # Remove whitespace around @ and dots, but only for email-like tokens.
    text = re.sub(
        r"([A-Za-z0-9._%+-]+)\s*@\s*([A-Za-z0-9.-]+)\s*\.\s*([A-Za-z]{2,})",
        r"\1@\2.\3",
        text,
    )

    return text


if __name__ == "__main__":
    from pathlib import Path

    base_dir = Path(__file__).resolve().parents[1]
    input_file = base_dir / "data" / "stress_test" / "pii_adversarial.md"
    original = input_file.read_text(encoding="utf-8")
    normalized = normalize_obfuscated_emails(original)

    print("=== EMAIL NORMALIZATION TEST ===")
    for line in normalized.splitlines():
        if any(marker in line for marker in (
            "alice@example.com",
            "bob.smith@example.com",
            "y.tanaka@hospital.org",
        )):
            print(line)
