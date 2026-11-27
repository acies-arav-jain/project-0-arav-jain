def chunk_words(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= size:
        raise ValueError("Overlap must be smaller than chunk size.")

    words = text.split()
    chunks = []
    step = size - overlap

    for start in range(0, len(words), step):
        end = start + size

        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        if end >= len(words):
            break

    return chunks