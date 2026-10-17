import numpy as np
from openai import OpenAI

MODEL = "text-embedding-3-small"

SENTENCES = [
    "Employees must obtain manager approval before planned leave.",
    "Emergency leave should be reported to the manager promptly.",
    "Employees should contact the IT helpdesk for technical issues.",
    "The IT helpdesk supports approved company devices.",
    "All employees must complete security awareness training.",
    "Training completion must be recorded by the employee's manager.",
]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def semantic_chunks(sentences, embeddings, threshold):
    if not sentences:
        return []

    chunks = []
    current = sentences[0]

    for i in range(len(sentences) - 1):
        score = cosine_similarity(embeddings[i], embeddings[i + 1])

        if score >= threshold:
            current += " " + sentences[i + 1]
        else:
            chunks.append(current)
            current = sentences[i + 1]

    chunks.append(current)
    return chunks


def main():
    client = OpenAI()
    response = client.embeddings.create(
        model=MODEL,
        input=SENTENCES,
    )

    embeddings = [
        np.array(item.embedding, dtype=float)
        for item in sorted(response.data, key=lambda item: item.index)
    ]

    print("Sentence count:", len(SENTENCES))

    for threshold in (0.3, 0.7, 0.9):
        chunks = semantic_chunks(SENTENCES, embeddings, threshold)
        print(f"\nThreshold: {threshold:.1f}")
        print("Chunk count:", len(chunks))

        for index, chunk in enumerate(chunks, start=1):
            print(f"  Chunk {index}: {chunk}")


if __name__ == "__main__":
    main()
