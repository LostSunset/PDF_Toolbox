"""
Reorder pages within a PDF.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pikepdf


@dataclass
class ReorderResult:
    """Result of a PDF page reorder operation."""

    success: bool
    message: str
    output_path: Path | None = None


def reorder_pdf(
    src: Path,
    dst: Path,
    new_order: list[int],
) -> ReorderResult:
    """
    Reorder pages of a PDF according to new_order.
    new_order: list of 0-based page indices in desired order.
    e.g. [2, 0, 1] means: page 3 first, then page 1, then page 2.
    """
    with pikepdf.open(str(src)) as pdf:
        total = len(pdf.pages)

        # Validate indices
        for idx in new_order:
            if idx < 0 or idx >= total:
                return ReorderResult(
                    False,
                    f"\u7121\u6548\u7684\u9801\u78bc\u7d22\u5f15: {idx + 1} "
                    f"(\u7e3d\u5171 {total} \u9801)",
                )

        new_pdf = pikepdf.Pdf.new()
        for idx in new_order:
            new_pdf.pages.append(pdf.pages[idx])
        new_pdf.save(str(dst))
        new_pdf.close()

    return ReorderResult(
        True,
        f"\u9801\u9762\u91cd\u6392\u5e8f\u5b8c\u6210\uff01\u5171 {len(new_order)} \u9801",
        dst,
    )


def get_page_count(pdf_path: Path) -> int:
    """Return page count of a PDF."""
    with pikepdf.open(str(pdf_path)) as pdf:
        return len(pdf.pages)
