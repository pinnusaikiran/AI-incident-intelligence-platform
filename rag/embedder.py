"""
Embedding generation.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from rag.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformer:

    return SentenceTransformer(
        EMBEDDING_MODEL
    )


def generate_embeddings(
    texts: list[str],
):

    model = get_embedder()

    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )