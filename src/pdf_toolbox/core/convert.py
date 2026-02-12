"""
PDF to PNG conversion via pdftoppm (poppler-utils).
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConvertResult:
    """Result of a PDF to PNG conversion."""

    success: bool
    message: str
    output_files: list[Path] = field(default_factory=list)


def find_pdftoppm() -> str | None:
    """Return the pdftoppm command name if available, else None."""
    try:
        subprocess.run(
            ["pdftoppm", "-v"],
            capture_output=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return "pdftoppm"
    except FileNotFoundError:
        return None


def convert_pdf_to_png(
    pdf_path: Path,
    output_dir: Path | None = None,
    dpi: int = 1200,
) -> ConvertResult:
    """
    Convert a single PDF to PNG files using pdftoppm.
    Output files are placed in output_dir (or same dir as PDF).
    """
    pdftoppm = find_pdftoppm()
    if pdftoppm is None:
        return ConvertResult(
            False,
            "\u627e\u4e0d\u5230 pdftoppm\uff0c\u8acb\u78ba\u8a8d\u5df2\u5b89\u88dd poppler-utils",
        )

    out_dir = output_dir or pdf_path.parent
    output_base = out_dir / pdf_path.stem

    cmd = [
        pdftoppm,
        "-png",
        "-r",
        str(dpi),
        str(pdf_path),
        str(output_base),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )

    if result.returncode != 0:
        return ConvertResult(
            False,
            f"\u8f49\u63db\u5931\u6557: {result.stderr.strip()}",
        )

    # Find generated PNG files
    output_files = sorted(out_dir.glob(f"{pdf_path.stem}*.png"))
    return ConvertResult(
        True,
        f"\u6210\u529f\u8f49\u63db {len(output_files)} \u9801",
        output_files,
    )
