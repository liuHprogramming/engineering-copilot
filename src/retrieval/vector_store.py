from pathlib import Path
import os
import sys

import chromadb
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))
# chunker.py currently imports pdf_reader as a top-level module when run in this repo layout.
sys.path.append(str(PROJECT_ROOT / "src" / "ingest"))

from ingest.pdf_reader import extract_pdf_pages
from ingest.chunker import chunk_pages

PDF_PATH = PROJECT_ROOT / "data" / "sample.pdf"
CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"
COLLECTION_NAME = "engineering_docs"
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "sentence-transformers/paraphrase-MiniLM-L3-v2",
)

def build_vector_store():
    pages = extract_pdf_pages(PDF_PATH)
    chunks = chunk_pages(pages)

    print(f"Total chunks: {len(chunks)}")
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...", flush=True)
    model_path = snapshot_download(repo_id=EMBEDDING_MODEL_NAME)
    model = SentenceTransformer(model_path, local_files_only=True)
    print("Embedding model loaded.", flush=True)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    texts = [c["text"] for c in chunks]
    print("Generating embeddings...", flush=True)
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    print("Embeddings generated.", flush=True)
    existing_ids = set(collection.get(include=[])["ids"])
    new_rows = [
        (
            chunk["chunk_id"],
            chunk["text"],
            {"page": chunk["page"], "source": chunk["source"]},
            embedding,
        )
        for chunk, embedding in zip(chunks, embeddings)
        if chunk["chunk_id"] not in existing_ids
    ]

    if new_rows:
        print(f"Writing {len(new_rows)} new chunks to ChromaDB...", flush=True)
        collection.add(
            ids=[row[0] for row in new_rows],
            documents=[row[1] for row in new_rows],
            metadatas=[row[2] for row in new_rows],
            embeddings=[row[3] for row in new_rows],
        )
    else:
        print("All chunks are already stored in ChromaDB.", flush=True)

    print("Vector database created successfully.")
    return collection


if __name__ == "__main__":
    build_vector_store()
