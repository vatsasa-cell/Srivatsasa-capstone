from pathlib import Path
from chunking_basics import load_html_text

def recursive_chunks(text: str, chunk_size: int = 100) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    chunks = []

    def split_piece(piece: str) -> None:
        piece = piece.strip()
        if not piece:
            return

        if len(piece) <= chunk_size:
            chunks.append(piece)
            return

        for separator in ("\n\n", "\n", ". ", " "):
            parts = piece.split(separator)
            if len(parts) > 1:
                current = ""

                for part in parts:
                    candidate = (
                        part if not current
                        else current + separator + part
                    )

                    if len(candidate) <= chunk_size:
                        current = candidate
                    else:
                        if current:
                            split_piece(current)
                        current = part

                if current:
                    split_piece(current)
                return

        # Fallback for a single unbroken string.
        chunks.append(piece[:chunk_size])
        split_piece(piece[chunk_size:])

    split_piece(text)
    return chunks

def main() -> None:
    text = load_html_text()
    chunks = recursive_chunks(text, chunk_size=100)

    print(f"Original characters: {len(text)}")
    print(f"Number of chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ({len(chunk)} characters) ---")
        print(chunk)

if __name__ == "__main__":
    main()
