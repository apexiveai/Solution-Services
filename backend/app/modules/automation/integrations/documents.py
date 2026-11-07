from pathlib import Path


SUPPORTED_DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv", ".txt"}


def validate_document_path(path: Path) -> Path:
    if path.suffix.lower() not in SUPPORTED_DOCUMENT_EXTENSIONS:
        raise ValueError("Unsupported document format.")
    return path
