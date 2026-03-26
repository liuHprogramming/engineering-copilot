from pathlib import Path
from typing import List, Dict

from pdf_reader import extract_pdf_pages

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF_PATH = PROJECT_ROOT / "data" / "sample.pdf"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping character-based chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def chunk_pages(pages: List[Dict], chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """
    Convert extracted pages into chunked documents with metadata.
    """
    all_chunks = []

    for page_data in pages:
        page_num = page_data["page"]
        source = page_data["source"]
        page_text = page_data["text"]

        page_chunks = chunk_text(page_text, chunk_size=chunk_size, overlap=overlap)

        for idx, chunk in enumerate(page_chunks):
            all_chunks.append(
                {
                    "chunk_id": f"{source}_p{page_num}_c{idx}",
                    "text": chunk,
                    "page": page_num,
                    "source": source,
                }
            )

    return all_chunks


if __name__ == "__main__":
    print(f"Using PDF: {DEFAULT_PDF_PATH}")

    pages = extract_pdf_pages(DEFAULT_PDF_PATH)
    chunks = chunk_pages(pages, chunk_size=500, overlap=100)

    print(f"Created {len(chunks)} chunks.\n")
    for chunk in chunks[:3]:
        print(chunk["chunk_id"])
        print(chunk["text"][:300])
        print("-" * 60)
