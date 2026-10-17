from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample_docs"


def load_html_text() -> str:
    from bs4 import BeautifulSoup

    path = SAMPLE_DIR / "product_page.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


def fixed_size_chunks(text: str, chunk_size: int = 100,
                      overlap: int = 20) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def main() -> None:
    text = load_html_text()
    chunks = fixed_size_chunks(text, chunk_size=100, overlap=20)

    print(f"Original characters: {len(text)}")
    print(f"Number of chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ({len(chunk)} characters) ---")
        print(repr(chunk))


if __name__ == "__main__":
    main()
