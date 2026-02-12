"""
Shared utility functions used across core modules.
"""

from __future__ import annotations

from pathlib import Path


def ensure_unique_path(path: Path) -> Path:
    """
    If path exists, append _1, _2, etc. before extension.
    "doc.pdf" -> "doc_1.pdf" -> "doc_2.pdf" ...
    """
    if not path.exists():
        return path
    stem = path.stem
    ext = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{ext}"
        if not candidate.exists():
            return candidate
        counter += 1


def validate_pdf(path: Path) -> bool:
    """Quick check: does the file exist, have .pdf extension, and start with %PDF?"""
    if not path.is_file():
        return False
    if path.suffix.lower() != ".pdf":
        return False
    try:
        with open(path, "rb") as f:
            header = f.read(5)
        return header == b"%PDF-"
    except OSError:
        return False


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
