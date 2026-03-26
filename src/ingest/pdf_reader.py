from pathlib import Path
import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF_PATH = PROJECT_ROOT / "data" / "sample.pdf"


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """
    Extract text page by page from a PDF.

    Returns:
        [
            {
                "page": 1,
                "text": "...",
                "source": "sample.pdf"
            },
            ...
        ]
    """
    path = Path(pdf_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages = []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:
                pages.append(
                    {
                        "page": i + 1,
                        "text": text,
                        "source": path.name,
                    }
                )

    return pages


if __name__ == "__main__":
    print(f"Using PDF: {DEFAULT_PDF_PATH}")

    pages = extract_pdf_pages(DEFAULT_PDF_PATH)

    print(f"Extracted {len(pages)} non-empty pages.\n")
    for page in pages[:2]:
        print(f"--- Page {page['page']} ---")
        print(page["text"][:800])
        print()
