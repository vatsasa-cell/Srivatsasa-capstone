from pathlib import Path

import pymupdf
import pdfplumber
import pytesseract
from PIL import Image

PDF_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "sample_docs"
    / "company_policies.pdf"
)


def extract_with_pymupdf(path: Path) -> list[str]:
    """Extract text separately from each PDF page."""
    with pymupdf.open(path) as pdf:
        return [page.get_text("text") for page in pdf]


def extract_with_pdfplumber(path: Path) -> list[str]:
    """Extract text separately from each PDF page."""
    with pdfplumber.open(path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def extract_with_ocr(path: Path, dpi: int = 200) -> list[str]:
    """Extract text from each PDF page using Tesseract OCR."""
    pages = []

    with pymupdf.open(path) as pdf:
        for page in pdf:
            scale = dpi / 72
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(scale, scale),
                alpha=False,
            )
            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples,
            )
            pages.append(pytesseract.image_to_string(image, lang="eng"))

    return pages


def extract_with_fallback(path: Path) -> list[str]:
    """Use PyMuPDF text extraction first; OCR pages with no text."""
    extracted_pages = extract_with_pymupdf(path)
    final_pages = []

    with pymupdf.open(path) as pdf:
        for index, text in enumerate(extracted_pages):
            if text.strip():
                final_pages.append(text)
            else:
                page = pdf[index]
                scale = 200 / 72
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(scale, scale),
                    alpha=False,
                )
                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples,
                )
                final_pages.append(
                    pytesseract.image_to_string(image, lang="eng")
                )

    return final_pages


def main() -> None:
    print(f"PDF: {PDF_PATH}")
    print(f"Exists: {PDF_PATH.exists()}")

    if not PDF_PATH.exists():
        raise FileNotFoundError(PDF_PATH)

    pymupdf_pages = extract_with_pymupdf(PDF_PATH)
    pdfplumber_pages = extract_with_pdfplumber(PDF_PATH)
    fallback_pages = extract_with_fallback(PDF_PATH)

    print("\n--- PyMuPDF ---")
    print(f"Pages: {len(pymupdf_pages)}")
    print(f"Characters: {sum(map(len, pymupdf_pages))}")
    print("\n".join(pymupdf_pages))

    print("\n--- pdfplumber ---")
    print(f"Pages: {len(pdfplumber_pages)}")
    print(f"Characters: {sum(map(len, pdfplumber_pages))}")
    print("\n".join(pdfplumber_pages))

    print("\n--- PyMuPDF + OCR fallback ---")
    print(f"Pages: {len(fallback_pages)}")
    print(f"Characters: {sum(map(len, fallback_pages))}")
    print("\n".join(fallback_pages))


if __name__ == "__main__":
    main()
