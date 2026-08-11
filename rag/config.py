"""
RAG configuration.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "rag_data" / "knowledge_base"

VECTOR_DB_DIR = PROJECT_ROOT / "artifacts" / "vector_store"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

LLM_BASE_URL = os.getenv(
    "LLM_BASE_URL",
    "http://localhost:11434/v1",
)

LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    "ollama",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2",
)

TOP_K = int(os.getenv("RAG_TOP_K", "5"))

CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "800"))

CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))