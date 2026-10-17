from pathlib import Path
import re
import numpy as np
from openai import OpenAI
import pymupdf

BASE_DIR = Path(__file__).parent.parent
PDF_PATH = BASE_DIR / "data" / "sample_docs" / "company_policies.pdf"
MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.45


def load_sentences() -> list[str]:
    with pymupdf.open(PDF_PATH) as pdf:
        text = "\n".join(page.get_text("text") for page in pdf)

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line == "Company Policies":
            continue
        if re.match(r"^Section \d+:", line):
            continue
        lines.append(line)

    text = " ".join(lines)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def semantic_chunks(
    sentences: list[str],
    embeddings: list[np.ndarray],
) -> list[str]:
    if not sentences:
        return []

    chunks = []
    current_chunk = sentences[0]

    for i in range(len(sentences) - 1):
        similarity = cosine_similarity(embeddings[i], embeddings[i + 1])
        print(
            f"Similarity: {similarity:.4f} | "
            f"Threshold: {SIMILARITY_THRESHOLD:.2f}"
        )

        if similarity >= SIMILARITY_THRESHOLD:
            current_chunk += " " + sentences[i + 1]
        else:
            chunks.append(current_chunk)
            current_chunk = sentences[i + 1]

    chunks.append(current_chunk)
    return chunks


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(PDF_PATH)

    sentences = load_sentences()
    print(f"Policy sentences: {len(sentences)}")

    for i, sentence in enumerate(sentences, start=1):
        print(f"{i}. {sentence}")

    if not sentences:
        raise ValueError("No sentences extracted from the policy PDF")

    client = OpenAI()
    response = client.embeddings.create(model=MODEL, input=sentences)
    embeddings = [
        np.array(item.embedding, dtype=float)
        for item in response.data
    ]

    chunks = semantic_chunks(sentences, embeddings)

    print(f"\nSemantic chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)


if __name__ == "__main__":
    main()
