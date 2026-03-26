# Engineering Copilot

Engineering Copilot is a compact Retrieval-Augmented Generation (RAG) project for engineering PDFs. It turns a PDF into a searchable vector store, retrieves the most relevant chunks for a question, and generates a grounded answer with citations.

This project is intentionally small and readable. The goal is to show the core moving parts of a RAG system clearly, without hiding them behind a large framework.

## Project Goal

The goal of this project is to build a system that can answer questions about an engineering PDF by using the document itself as evidence.

Instead of asking an LLM to answer from memory alone, this project first retrieves relevant text from the PDF and then gives that retrieved context to the model. That makes the final answer more grounded, more relevant to the document, and easier to trace back to a source page.

In short, this project demonstrates how to build an end-to-end document question-answering pipeline:

```text
PDF -> page extraction -> chunking -> embeddings -> ChromaDB -> retrieval -> LLM answer
```

## Core Idea

Large language models are powerful, but they can still:

- answer from general knowledge instead of your document
- miss important details in long PDFs
- hallucinate facts that are not actually in the source material

RAG helps solve this by adding a retrieval step before generation:

1. read the PDF
2. split it into smaller chunks
3. convert those chunks into embeddings
4. store them in a vector database
5. retrieve the most relevant chunks for a user question
6. ask the LLM to answer using the retrieved chunks as context

That is the main idea behind this project: combine document retrieval with LLM generation so answers are grounded in the actual engineering document.

## Why This Project Matters

This project is useful because it demonstrates the practical ideas behind modern document-based AI systems:

- extracting text from source documents
- preserving page-level metadata for citation
- chunking text into retrievable units
- embedding chunks into vector space
- retrieving semantically relevant context
- generating grounded answers from retrieved evidence

It is also a good learning project because it keeps the pipeline simple enough to understand end to end:

- what data is stored
- how retrieval works
- why embeddings are needed
- where citations come from
- how an LLM can be connected to external knowledge

## Current Capabilities

- PDF text extraction with page numbers
- overlapping chunking for context preservation
- sentence-transformer embeddings
- persistent ChromaDB vector storage
- semantic retrieval over embedded chunks
- OpenAI answer generation with source citations

## Architecture

### Ingestion

- `src/ingest/pdf_reader.py`: extracts page-level text from the PDF
- `src/ingest/chunker.py`: splits each page into overlapping chunks
- `src/retrieval/vector_store.py`: embeds chunks and stores them in a persistent Chroma collection

### Retrieval

- `src/retrieval/retriever.py`: embeds a user query and returns the top matching chunks from ChromaDB

### Generation

- `src/generation/answer_generator.py`: builds a context block from retrieved chunks and asks the LLM to answer with citations
- `src/main.py`: simple command-line entry point for the full flow

## Project Structure

```text
src/
  ingest/
    pdf_reader.py
    chunker.py
  retrieval/
    vector_store.py
    retriever.py
  generation/
    answer_generator.py
  main.py
data/
  sample.pdf
```

## Default Sample Document

The repository includes a public engineering paper as the default sample PDF:

- `data/sample.pdf`
- Title: `Engineering Properties of Treated Natural Hemp Fiber-Reinforced Concrete`
- Authors: Xiangming Zhou, Harmeet Saini, and Gediminas Kastiukas
- Publisher: Frontiers
- License: CC BY

Article page:

- [Frontiers article](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2017.00033/full)

Attribution:

- Zhou, X., Saini, H., and Kastiukas, G. (2017). `Engineering Properties of Treated Natural Hemp Fiber-Reinforced Concrete`. Frontiers in Built Environment. Used here under the CC BY license.

## Tech Stack

- Python
- PyMuPDF
- Sentence Transformers
- ChromaDB
- OpenAI API

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key for the answer generation step:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Optional configuration:

```bash
export OPENAI_MODEL=gpt-4o-mini
export EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-MiniLM-L3-v2
```

## How To Run

### 1. Build the vector store

This reads `data/sample.pdf`, extracts page text, chunks it, embeds the chunks, and stores them in ChromaDB.

```bash
python src/retrieval/vector_store.py
```

### 2. Test retrieval only

This runs a sample query against the stored vector database and prints the top matching chunks.

```bash
python src/retrieval/retriever.py
```

### 3. Run the full pipeline

This builds the vector store if needed, retrieves relevant chunks, and asks the LLM to answer using only the retrieved context.

```bash
python src/main.py "What are the main instructions in this document?"
```

## Example Workflow

```bash
source .venv/bin/activate
python src/retrieval/vector_store.py
python src/main.py "What does the document say about the mechanical properties of treated hemp fiber-reinforced concrete?"
```

## Design Decisions

- Page-level extraction is preserved so answers can cite document pages.
- Chunk overlap is used to reduce context loss at chunk boundaries.
- ChromaDB is persisted locally so indexing and retrieval can happen in separate runs.
- The same embedding model should be used for both indexing and retrieval.
- The code stays intentionally simple and script-oriented for clarity.

## Limitations

- The project currently uses a single sample PDF by default.
- Retrieval quality depends on the chosen embedding model and chunking settings.
- Answer generation requires an `OPENAI_API_KEY`.
- There is no UI yet; interaction is through the terminal.

## Future Improvements

- support multiple documents
- add evaluation scripts for retrieval quality
- expose the pipeline through a small web app
- improve prompt formatting and citation display

## Notes

- Chroma data is stored locally in `data/chroma/`
- the first embedding-model download may take some time
- later runs reuse the local Hugging Face cache
