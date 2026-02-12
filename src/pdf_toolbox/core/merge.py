"""
Merge multiple PDFs into one.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pikepdf


@dataclass
class MergeResult:
    """Result of a PDF merge operation."""

    success: bool
    message: str
    output_path: Path | None = None
    page_count: int = 0


def merge_pdfs(
    input_files: list[Path],
    output_path: Path,
) -> MergeResult:
    """Merge multiple PDFs in order into a single file."""
    if not input_files:
        return MergeResult(False, "\u6c92\u6709\u6a94\u6848\u9700\u8981\u5408\u4f75\u3002")

    try:
        merged = pikepdf.Pdf.new()
        total_pages = 0

        for pdf_path in input_files:
            with pikepdf.open(str(pdf_path)) as src:
                merged.pages.extend(src.pages)
                total_pages += len(src.pages)

        merged.save(str(output_path))
        merged.close()

        return MergeResult(
            True,
            f"\u5408\u4f75\u5b8c\u6210\uff01\u5171 {len(input_files)} \u500b\u6a94\u6848\uff0c"
            f"{total_pages} \u9801",
            output_path,
            total_pages,
        )
    except Exception as exc:
        return MergeResult(False, f"\u5408\u4f75\u5931\u6557: {exc}")
