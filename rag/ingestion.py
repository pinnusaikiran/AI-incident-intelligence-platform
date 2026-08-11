"""
Knowledge-base ingestion pipeline.
"""

from rag.config import KNOWLEDGE_BASE_DIR
from rag.document_loader import load_documents
from rag.chunker import chunk_text
from rag.embedder import generate_embeddings
from rag.vector_store import add_documents


def ingest():

    documents = load_documents(
        KNOWLEDGE_BASE_DIR
    )

    all_chunks = []

    for source, text in documents:

        chunks = chunk_text(
            text=text,
            source=source,
        )

        all_chunks.extend(chunks)

    if not all_chunks:
        raise RuntimeError(
            "No documents found in knowledge base."
        )

    texts = [
        chunk.text
        for chunk in all_chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    ids = [
        chunk.chunk_id
        for chunk in all_chunks
    ]

    metadatas = [
        {
            "source": chunk.source
        }
        for chunk in all_chunks
    ]

    add_documents(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Ingested {len(all_chunks)} chunks."
    )


if __name__ == "__main__":
    ingest()