from pathlib import Path
import os
import sys

import chromadb
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))

from retrieval.vector_store import CHROMA_PATH, COLLECTION_NAME

EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "sentence-transformers/paraphrase-MiniLM-L3-v2",
)


def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    model_path = snapshot_download(repo_id=EMBEDDING_MODEL_NAME)
    model = SentenceTransformer(model_path, local_files_only=True)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return [
        {
            "text": document,
            "page": metadata["page"],
            "source": metadata["source"],
            "score": distance,
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


if __name__ == "__main__":
    sample_query = "What does this document say?"
    chunks = retrieve_chunks(sample_query, top_k=3)

    print(f"Query: {sample_query}\n")
    for index, chunk in enumerate(chunks, start=1):
        print(f"Result {index} | source={chunk['source']} | page={chunk['page']}")
        print(f"Score: {chunk['score']}")
        print(chunk["text"][:400])
        print("-" * 60)
