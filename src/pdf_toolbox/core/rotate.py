"""
Rotate PDF pages by 90/180/270 degrees.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pikepdf


@dataclass
class RotateResult:
    """Result of a PDF rotation operation."""

    success: bool
    message: str
    output_path: Path | None = None


def rotate_pdf(
    src: Path,
    dst: Path,
    degrees: int,
    page_indices: list[int] | None = None,
) -> RotateResult:
    """
    Rotate pages of a PDF by the specified degrees.
    page_indices: 0-based list of pages to rotate. None = all pages.
    degrees: must be 90, 180, or 270.
    """
    if degrees not in (90, 180, 270):
        return RotateResult(False, f"\u7121\u6548\u7684\u65cb\u8f49\u89d2\u5ea6: {degrees}")

    with pikepdf.open(str(src)) as pdf:
        total = len(pdf.pages)
        targets = page_indices if page_indices is not None else list(range(total))
        rotated_count = 0

        for idx in targets:
            if 0 <= idx < total:
                page = pdf.pages[idx]
                current = int(page.get("/Rotate", 0))
                page["/Rotate"] = (current + degrees) % 360
                rotated_count += 1

        pdf.save(str(dst))

    return RotateResult(
        True,
        f"\u65cb\u8f49\u5b8c\u6210\uff01\u5171\u65cb\u8f49 {rotated_count} \u9801 {degrees}\u00b0",
        dst,
    )
