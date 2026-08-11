"""
RAG service.

Orchestrates retrieval and LLM generation.
"""

from rag.models import RAGResponse
from rag.retriever import retrieve
from rag.prompt_builder import build_prompt
from rag.llm_client import generate_answer


class RAGService:
    def ask(
    self,
    question: str,
    incident_context: dict | None = None,
    ):
        
        """
        Retrieve relevant knowledge and generate
        a grounded answer.
        """

        results = retrieve(question)

        prompt = build_prompt(
            question=question,
            contexts=results,
            incident_context=incident_context,
        )

        answer = generate_answer(prompt)

        return RAGResponse(
            answer=answer,
            sources=results,
        )