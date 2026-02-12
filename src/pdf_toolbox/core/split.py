"""
Split a PDF by page ranges, every N pages, or extract specific pages.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

import pikepdf


class SplitMode(Enum):
    """How to split the PDF."""

    BY_RANGE = auto()
    EVERY_N_PAGES = auto()
    EXTRACT_PAGES = auto()


@dataclass
class SplitResult:
    """Result of a PDF split operation."""

    success: bool
    message: str
    output_files: list[Path] = field(default_factory=list)


def parse_page_ranges(spec: str, total_pages: int) -> list[tuple[int, int]]:
    """
    Parse "1-3, 5, 7-10" into [(0,2), (4,4), (6,9)] (0-based inclusive).
    """
    ranges: list[tuple[int, int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = max(0, int(start_s.strip()) - 1)
            end = min(total_pages - 1, int(end_s.strip()) - 1)
            if start <= end:
                ranges.append((start, end))
        else:
            page = int(part) - 1
            if 0 <= page < total_pages:
                ranges.append((page, page))
    return ranges


def get_page_count(pdf_path: Path) -> int:
    """Return page count without loading entire PDF."""
    with pikepdf.open(str(pdf_path)) as pdf:
        return len(pdf.pages)


def split_pdf(
    src: Path,
    output_dir: Path,
    mode: SplitMode,
    *,
    page_ranges: str = "",
    pages_per_split: int = 1,
    page_numbers: list[int] | None = None,
) -> SplitResult:
    """Split a PDF according to the specified mode."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_files: list[Path] = []

    with pikepdf.open(str(src)) as pdf:
        total = len(pdf.pages)

        if mode == SplitMode.BY_RANGE:
            ranges = parse_page_ranges(page_ranges, total)
            if not ranges:
                return SplitResult(False, "\u7121\u6548\u7684\u9801\u78bc\u7bc4\u570d\u3002")
            for start, end in ranges:
                out_pdf = pikepdf.Pdf.new()
                for page_idx in range(start, end + 1):
                    out_pdf.pages.append(pdf.pages[page_idx])
                out_path = output_dir / f"{src.stem}_p{start + 1}-{end + 1}.pdf"
                out_pdf.save(str(out_path))
                out_pdf.close()
                output_files.append(out_path)

        elif mode == SplitMode.EVERY_N_PAGES:
            n = max(1, pages_per_split)
            for chunk_start in range(0, total, n):
                chunk_end = min(chunk_start + n, total)
                out_pdf = pikepdf.Pdf.new()
                for page_idx in range(chunk_start, chunk_end):
                    out_pdf.pages.append(pdf.pages[page_idx])
                out_path = output_dir / f"{src.stem}_p{chunk_start + 1}-{chunk_end}.pdf"
                out_pdf.save(str(out_path))
                out_pdf.close()
                output_files.append(out_path)

        elif mode == SplitMode.EXTRACT_PAGES:
            indices = page_numbers or []
            if not indices:
                return SplitResult(
                    False, "\u672a\u6307\u5b9a\u8981\u63d0\u53d6\u7684\u9801\u78bc\u3002"
                )
            out_pdf = pikepdf.Pdf.new()
            valid_pages = [p for p in indices if 0 <= p < total]
            for page_idx in valid_pages:
                out_pdf.pages.append(pdf.pages[page_idx])
            pages_str = ",".join(str(p + 1) for p in valid_pages)
            out_path = output_dir / f"{src.stem}_extracted_p{pages_str}.pdf"
            out_pdf.save(str(out_path))
            out_pdf.close()
            output_files.append(out_path)

    return SplitResult(
        True,
        f"\u62c6\u5206\u5b8c\u6210\uff0c\u7522\u751f {len(output_files)} \u500b\u6a94\u6848\u3002",
        output_files,
    )
