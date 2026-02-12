"""
Compress PDF by reducing image resolution and removing metadata.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class CompressionLevel(Enum):
    """Compression level presets."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    MAXIMUM = auto()


# Ghostscript PDFSETTINGS mapping
_GS_SETTINGS = {
    CompressionLevel.LOW: "/prepress",
    CompressionLevel.MEDIUM: "/printer",
    CompressionLevel.HIGH: "/ebook",
    CompressionLevel.MAXIMUM: "/screen",
}


@dataclass
class CompressResult:
    """Result of a PDF compression operation."""

    success: bool
    message: str
    output_path: Path | None = None
    original_size: int = 0
    compressed_size: int = 0

    @property
    def reduction_percent(self) -> float:
        if self.original_size == 0:
            return 0.0
        return (1 - self.compressed_size / self.original_size) * 100


def _find_ghostscript() -> str | None:
    """Find the Ghostscript command."""
    for cmd in ("gs", "gswin64c", "gswin32c", "ghostscript"):
        try:
            subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
            return cmd
        except FileNotFoundError, subprocess.CalledProcessError:
            continue
    return None


def compress_pdf(
    src: Path,
    dst: Path,
    level: CompressionLevel = CompressionLevel.MEDIUM,
    remove_metadata: bool = True,
) -> CompressResult:
    """
    Compress PDF using Ghostscript.
    Falls back to PyMuPDF if Ghostscript is not available.
    """
    original_size = src.stat().st_size

    # Try Ghostscript first
    gs_cmd = _find_ghostscript()
    if gs_cmd:
        return _compress_with_gs(src, dst, gs_cmd, level, original_size)

    # Fallback to PyMuPDF
    return _compress_with_pymupdf(src, dst, level, original_size, remove_metadata)


def _compress_with_gs(
    src: Path,
    dst: Path,
    gs_cmd: str,
    level: CompressionLevel,
    original_size: int,
) -> CompressResult:
    """Compress using Ghostscript."""
    setting = _GS_SETTINGS[level]
    cmd = [
        gs_cmd,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={setting}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={dst}",
        str(src),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )

    if result.returncode == 0 and dst.exists():
        compressed_size = dst.stat().st_size
        cr = CompressResult(
            True,
            "",
            dst,
            original_size,
            compressed_size,
        )
        cr.message = f"\u58d3\u7e2e\u5b8c\u6210\uff01\u6e1b\u5c11 {cr.reduction_percent:.1f}%"
        return cr

    return CompressResult(
        False, f"\u58d3\u7e2e\u5931\u6557: {result.stderr.strip()}", None, original_size, 0
    )


def _compress_with_pymupdf(
    src: Path,
    dst: Path,
    level: CompressionLevel,
    original_size: int,
    remove_metadata: bool,
) -> CompressResult:
    """Compress using PyMuPDF."""
    import fitz

    doc = fitz.open(str(src))
    try:
        if remove_metadata:
            doc.set_metadata({})

        # Save with compression options
        garbage = {
            CompressionLevel.LOW: 1,
            CompressionLevel.MEDIUM: 2,
            CompressionLevel.HIGH: 3,
            CompressionLevel.MAXIMUM: 4,
        }[level]

        doc.save(
            str(dst),
            garbage=garbage,
            deflate=True,
            clean=True,
        )
    finally:
        doc.close()

    compressed_size = dst.stat().st_size
    cr = CompressResult(True, "", dst, original_size, compressed_size)
    cr.message = f"\u58d3\u7e2e\u5b8c\u6210\uff01\u6e1b\u5c11 {cr.reduction_percent:.1f}%"
    return cr
