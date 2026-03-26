# Engineering Copilot

## Project Goal

This project builds a **Retrieval-Augmented Generation (RAG)** system for engineering PDFs.

The system allows a user to ask questions about engineering documents and receive answers grounded in the document content rather than relying only on the LLM's internal knowledge.

The goal of the project is to build a **clean, understandable end-to-end RAG pipeline** that demonstrates AI engineering skills.

---

# Core Idea

The system works in two phases.

## 1. Ingestion Pipeline (offline)

Documents are processed and stored as embeddings.

Pipeline:

PDF  
→ page extraction  
→ chunking  
→ embeddings  
→ vector database

This converts documents into a searchable knowledge base.

## 2. Retrieval + Generation Pipeline (runtime)

When a user asks a question:

query  
→ query embedding  
→ vector similarity search  
→ retrieve relevant chunks  
→ send context to LLM  
→ generate grounded answer with citations

---

# Project Folder Structure

engineering-copilot/

data/

- sample.pdf

src/

ingest/

- pdf_reader.py
- chunker.py

retrieval/

- vector_store.py

generation/

- (future LLM answer generation)

eval/

- (future evaluation tools)

notebooks/

- experiments

tests/

- unit tests

README.md  
requirements.txt  
PROJECT_CONTEXT.md

---

# What Each Module Does

## src/ingest/pdf_reader.py

Responsible for extracting text from PDFs page by page.

Main function:

extract_pdf_pages(pdf_path)

Expected output format:

```python
[
    {
        "page": 1,
        "text": "page text here",
        "source": "sample.pdf"
    }
]
```

Page-level extraction is used so the system can later provide **citations with page numbers**.

---

## src/ingest/chunker.py

Responsible for splitting page text into overlapping chunks.

Main functions:

chunk_text(text, chunk_size=500, overlap=100)

chunk_pages(pages, chunk_size=500, overlap=100)

Expected output format:

```python
[
    {
        "chunk_id": "sample.pdf_p3_c0",
        "text": "chunk text here",
        "page": 3,
        "source": "sample.pdf"
    }
]
```

Chunking is necessary because:

- embedding models work better with smaller text segments
- retrieval works better on smaller semantic units
- long documents are difficult to process directly

Overlap is used to prevent losing context at chunk boundaries.

---

## src/retrieval/vector_store.py

Responsible for:

- loading extracted pages
- chunking the text
- generating embeddings
- storing embeddings and metadata in the vector database

Embedding model:

sentence-transformers/all-MiniLM-L6-v2

Vector database:

ChromaDB

Each stored record contains:

- embedding vector
- text chunk
- metadata (page number, source file)
- chunk id

---

# Current Implementation Status

Already implemented:

✔ project environment setup  
✔ PDF text extraction  
✔ page-level metadata  
✔ chunking with overlap  
✔ chunk metadata structure

Currently implementing:

- embedding chunks
- storing embeddings in the vector database

Not implemented yet:

- query embedding
- retrieval of top-k relevant chunks
- LLM prompt construction
- LLM answer generation
- answer citations
- evaluation pipeline
- UI interface

---

# Current Data Flow

The system currently processes data as:

PDF  
→ page extraction  
→ chunking  
→ embeddings  
→ vector database

The final RAG pipeline will be:

PDF  
→ page extraction  
→ chunking  
→ embeddings  
→ vector database  
→ query embedding  
→ vector retrieval  
→ LLM prompt with retrieved context  
→ grounded answer with citations

---

# Important Design Decisions

1. Text is extracted page by page so page numbers can later be used as citations.

2. Chunking uses overlap to preserve context across chunk boundaries.

3. Each chunk stores metadata including:
   - page number
   - source file
   - chunk id

4. The system architecture should remain simple and easy to understand.

This project is meant to demonstrate **AI engineering concepts**, not to build a large production framework.

---

# Coding Rules for This Project

When modifying code:

- preserve the current folder structure
- preserve page and source metadata
- keep functions simple and readable
- avoid unnecessary abstractions
- avoid rewriting working ingestion code
- do not replace Chroma unless explicitly requested

Prefer **small fixes instead of large architectural changes**.

---

# What Coding Assistants Should Know

This repository implements a **simple educational RAG system**.

The goal is to build a clean pipeline that demonstrates:

- document ingestion
- chunking
- embedding generation
- vector search
- LLM-based question answering

The focus is **clarity and correctness**, not building a large production framework.
