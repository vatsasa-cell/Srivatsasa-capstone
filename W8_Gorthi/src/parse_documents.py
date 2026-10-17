
from pathlib import Path
from bs4 import BeautifulSoup
from docx import Document

BASE_DIR = Path(__file__).parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample_docs"


def parse_html(path: Path) -> str:
    soup = BeautifulSoup(
        path.read_text(encoding="utf-8"),
        "html.parser",
    )

    # Remove page elements that are usually not useful
    # as knowledge content.
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


def parse_docx(path: Path) -> str:
    document = Document(path)
    lines = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            lines.append(text)

    return "\n".join(lines)


def main() -> None:
    html_path = SAMPLE_DIR / "product_page.html"
    docx_path = SAMPLE_DIR / "onboarding.docx"

    for path in (html_path, docx_path):
        if not path.exists():
            raise FileNotFoundError(path)

    html_text = parse_html(html_path)
    docx_text = parse_docx(docx_path)

    print("=== HTML extraction ===")
    print(html_text)
    print(f"HTML characters: {len(html_text)}")

    print("\n=== DOCX extraction ===")
    print(docx_text)
    print(f"DOCX characters: {len(docx_text)}")


if __name__ == "__main__":
    main()
