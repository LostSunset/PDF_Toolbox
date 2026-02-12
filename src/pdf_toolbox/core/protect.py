"""
PDF copy-protection: disable text extraction / copy.
Uses dual-layer encryption (pikepdf + PyPDF2).
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import pikepdf
from PyPDF2 import PdfReader, PdfWriter


@dataclass
class ProtectResult:
    """Result of a PDF protection operation."""

    success: bool
    message: str
    output_path: Path | None = None


def protect_pdf(
    src: Path,
    dst: Path,
    user_password: str = "",
    owner_password: str = "",
) -> ProtectResult:
    """
    Apply dual-layer encryption to disable copy.

    Layer 1 (pikepdf): Set extract=False permission.
    Layer 2 (PyPDF2): Encrypt with permissions_flag=2052 (allow print, deny copy).
    """
    # Use a proper temporary file instead of hardcoded "temp_p.pdf"
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        temp_path = Path(tmp.name)

    try:
        # Layer 1: pikepdf
        with pikepdf.open(str(src)) as pdf:
            permissions = pikepdf.Permissions(extract=False)
            pdf.save(
                str(temp_path),
                encryption=pikepdf.Encryption(
                    user=user_password,
                    owner=owner_password,
                    allow=permissions,
                ),
            )

        # Layer 2: PyPDF2
        reader = PdfReader(str(temp_path))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # permissions_flag=2052: allow printing, deny copying
        writer.encrypt(user_password, owner_password, permissions_flag=2052)

        with open(dst, "wb") as output_file:
            writer.write(output_file)

        return ProtectResult(
            True,
            f"\u4fdd\u8b77\u5b8c\u6210: {dst.name}",
            dst,
        )

    finally:
        if temp_path.exists():
            temp_path.unlink()


def generate_protected_path(src: Path, output_dir: Path | None = None) -> Path:
    """Generate output path for protected PDF (adds _p suffix)."""
    from pdf_toolbox.core.utils import ensure_unique_path

    parent = output_dir or src.parent
    output = parent / f"{src.stem}_p{src.suffix}"
    return ensure_unique_path(output)
