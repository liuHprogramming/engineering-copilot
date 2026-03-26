import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from generation.answer_generator import generate_answer
from retrieval.vector_store import build_vector_store


def main():
    parser = argparse.ArgumentParser(description="Ask questions about the sample engineering PDF.")
    parser.add_argument("query", help="Question to ask about the document.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve.")
    args = parser.parse_args()

    build_vector_store()
    result = generate_answer(args.query, top_k=args.top_k)

    print("\nAnswer:\n")
    print(result["answer"])
    print("\nSources:\n")
    for chunk in result["chunks"]:
        print(f"- {chunk['source']} page {chunk['page']}")


if __name__ == "__main__":
    main()
