"""
Document loading utilities for the RAG knowledge base.
"""

from pathlib import Path

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
}


def load_text_file(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def load_docx(path: Path) -> str:
    document = Document(str(path))

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def load_document(path: Path) -> str:

    extension = path.suffix.lower()

    if extension in {".txt", ".md"}:
        return load_text_file(path)

    if extension == ".pdf":
        return load_pdf(path)

    if extension == ".docx":
        return load_docx(path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )


def load_documents(directory: Path) -> list[tuple[str, str]]:

    documents = []

    for path in directory.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = load_document(path)

        if text.strip():
            documents.append(
                (
                    str(path),
                    text,
                )
            )

    return documents