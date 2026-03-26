from pathlib import Path
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))

from retrieval.retriever import retrieve_chunks

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def build_context(chunks: list[dict]) -> str:
    return "\n\n".join(
        [
            (
                f"[Chunk {index}] "
                f"Source: {chunk['source']}, Page: {chunk['page']}\n"
                f"{chunk['text']}"
            )
            for index, chunk in enumerate(chunks, start=1)
        ]
    )


def generate_answer(query: str, top_k: int = 3) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    chunks = retrieve_chunks(query, top_k=top_k)
    context = build_context(chunks)

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You answer questions using only the provided document context. "
                    "If the answer is not in the context, say that clearly. "
                    "Cite sources using the format (source, page X)."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {query}\n\nContext:\n{context}",
            },
        ],
    )

    return {
        "answer": response.output_text,
        "chunks": chunks,
    }


if __name__ == "__main__":
    sample_query = "Summarize the main points in this document."
    result = generate_answer(sample_query, top_k=3)

    print("Answer:\n")
    print(result["answer"])
