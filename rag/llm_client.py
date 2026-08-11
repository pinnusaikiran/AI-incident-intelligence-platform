"""
LLM client.
"""

from functools import lru_cache

from openai import OpenAI

from rag.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
)


@lru_cache(maxsize=1)
def get_llm_client() -> OpenAI:

    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
    )


def generate_answer(
    prompt: str,
) -> str:

    client = get_llm_client()

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content or ""