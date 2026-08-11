"""
Text chunking utilities.
"""

from rag.config import CHUNK_SIZE, CHUNK_OVERLAP
from rag.models import DocumentChunk


def chunk_text(
    text: str,
    source: str,
) -> list[DocumentChunk]:

    chunks = []

    start = 0
    chunk_number = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(
                DocumentChunk(
                    text=chunk,
                    source=source,
                    chunk_id=f"{source}:{chunk_number}",
                )
            )

        chunk_number += 1

        start = end - CHUNK_OVERLAP

        if start < 0:
            start = 0

    return chunks