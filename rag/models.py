"""
RAG domain models.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DocumentChunk:
    text: str
    source: str
    chunk_id: str


@dataclass
class RetrievedDocument:
    text: str
    source: str
    score: float


@dataclass
class RAGResponse:
    answer: str
    sources: List[RetrievedDocument]