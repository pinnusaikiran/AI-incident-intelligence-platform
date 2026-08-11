"""
Vector database management.
"""

from functools import lru_cache

import chromadb

from rag.config import VECTOR_DB_DIR


COLLECTION_NAME = "incident_knowledge"


@lru_cache(maxsize=1)
def get_vector_client():

    return chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )


def get_collection():

    client = get_vector_client()

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": (
                "Knowledge base for "
                "AI Incident Intelligence Platform"
            )
        },
    )


def add_documents(
    ids: list[str],
    documents: list[str],
    embeddings,
    metadatas: list[dict],
):

    collection = get_collection()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )


def search(
    query_embedding,
    top_k: int,
):

    collection = get_collection()

    result = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
    )

    documents = result.get(
        "documents",
        [[]],
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]],
    )[0]

    distances = result.get(
        "distances",
        [[]],
    )[0]

    return list(
        zip(
            documents,
            metadatas,
            distances,
        )
    )