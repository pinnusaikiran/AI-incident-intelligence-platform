"""
Knowledge retrieval.
"""

from rag.config import TOP_K
from rag.embedder import generate_embeddings
from rag.vector_store import search

from rag.models import RetrievedDocument


def retrieve(
    query: str,
    top_k: int = TOP_K,
) -> list[RetrievedDocument]:

    embedding = generate_embeddings(
        [query]
    )[0]

    results = search(
        query_embedding=embedding,
        top_k=top_k,
    )

    retrieved = []

    for document, metadata, distance in results:

        retrieved.append(
            RetrievedDocument(
                text=document,
                source=metadata.get(
                    "source",
                    "unknown",
                ),
                score=float(distance),
            )
        )

    return retrieved