
from pathlib import Path
from bs4 import BeautifulSoup
from docx import Document

BASE_DIR = Path(__file__).parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample_docs"

HTML_PATH = SAMPLE_DIR / "product_page.html"
DOCX_PATH = SAMPLE_DIR / "onboarding.docx"


def structure_aware_html_chunks() -> list[dict[str, str]]:
    """Create chunks from HTML headings and their following content."""
    html = HTML_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    chunks = []

    title = soup.find("title")
    if title and title.get_text(strip=True):
        chunks.append({
            "section": "Page Title",
            "text": title.get_text(" ", strip=True),
        })

    for heading in soup.find_all(["h1", "h2", "h3"]):
        section_name = heading.get_text(" ", strip=True)
        content = []

        for sibling in heading.find_next_siblings():
            if sibling.name in ["h1", "h2", "h3"]:
                break

            text = sibling.get_text(" ", strip=True)
            if text:
                content.append(text)

        if content:
            chunks.append({
                "section": section_name,
                "text": " ".join(content),
            })

    return chunks


def structure_aware_docx_chunks() -> list[dict[str, str]]:
    """Create chunks using DOCX heading styles as section boundaries."""
    document = Document(DOCX_PATH)

    chunks = []
    heading_stack = []
    current_paragraphs = []

    def save_current_section() -> None:
        if not current_paragraphs:
            return

        chunks.append({
            "section": " > ".join(heading_stack) or "Document Body",
            "text": "\n".join(current_paragraphs),
        })

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        style_name = paragraph.style.name if paragraph.style else ""
        is_heading = style_name.startswith("Heading ")

        if is_heading:
            save_current_section()
            current_paragraphs = []

            try:
                level = int(style_name.split()[-1])
            except ValueError:
                level = 1

            # Keep parent headings and replace headings at this level.
            heading_stack = heading_stack[:level - 1]
            heading_stack.append(text)
        else:
            current_paragraphs.append(text)

    save_current_section()
    return chunks


def main() -> None:
    if not HTML_PATH.exists():
        raise FileNotFoundError(HTML_PATH)
    if not DOCX_PATH.exists():
        raise FileNotFoundError(DOCX_PATH)

    for label, chunks in (
        ("HTML structure-aware chunks", structure_aware_html_chunks()),
        ("DOCX structure-aware chunks", structure_aware_docx_chunks()),
    ):
        print(f"\n=== {label} ===")
        print(f"Number of chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):
            print(f"\n--- Chunk {index} ---")
            print(f"Section: {chunk['section']}")
            print(f"Text: {chunk['text']}")


if __name__ == "__main__":
    main()
