"""
PDF unlock and repair -- multi-engine chain.
Ported from pdf_unlocker_007_(work).py, stripped of all UI and pip logic.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class RepairEngine(Enum):
    """Available PDF repair engines."""

    PYMUPDF = auto()
    PYPDF2 = auto()
    PIKEPDF = auto()
    GHOSTSCRIPT = auto()
    SIMPLE_COPY = auto()


@dataclass
class RepairResult:
    """Result of a PDF repair attempt."""

    success: bool
    engine: RepairEngine | None
    message: str
    output_path: Path | None = None


def _repair_with_pymupdf(src: Path, dst: Path, password: str | None = None) -> RepairResult:
    """Repair using PyMuPDF (fitz)."""
    import fitz

    doc = fitz.open(str(src))
    try:
        if doc.needs_pass:
            doc.authenticate(password or "")
        new_doc = fitz.open()
        new_doc.insert_pdf(doc)
        new_doc.save(str(dst))
        new_doc.close()
    finally:
        doc.close()
    return RepairResult(True, RepairEngine.PYMUPDF, "PyMuPDF \u4fee\u5fa9\u6210\u529f", dst)


def _repair_with_pypdf2(src: Path, dst: Path, password: str | None = None) -> RepairResult:
    """Repair using PyPDF2."""
    from PyPDF2 import PdfReader, PdfWriter

    with open(src, "rb") as f:
        reader = PdfReader(f)
        if reader.is_encrypted:
            reader.decrypt(password or "")
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(dst, "wb") as out:
            writer.write(out)
    return RepairResult(True, RepairEngine.PYPDF2, "PyPDF2 \u4fee\u5fa9\u6210\u529f", dst)


def _repair_with_pikepdf(src: Path, dst: Path, password: str | None = None) -> RepairResult:
    """Repair using pikepdf."""
    import pikepdf

    with pikepdf.open(str(src), password=password or "", allow_overwriting_input=True) as pdf:
        pdf.save(str(dst))
    return RepairResult(True, RepairEngine.PIKEPDF, "pikepdf \u4fee\u5fa9\u6210\u529f", dst)


def _find_ghostscript() -> str | None:
    """Find the Ghostscript command on this system."""
    gs_commands = ["gs", "gswin64c", "gswin32c", "ghostscript"]
    for cmd in gs_commands:
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


def _repair_with_ghostscript(src: Path, dst: Path, password: str | None = None) -> RepairResult:
    """Repair using Ghostscript."""
    gs_cmd = _find_ghostscript()
    if not gs_cmd:
        return RepairResult(False, RepairEngine.GHOSTSCRIPT, "Ghostscript \u672a\u5b89\u88dd")

    cmd = [
        gs_cmd,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/prepress",
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
    if result.returncode == 0 and dst.exists() and dst.stat().st_size > 0:
        return RepairResult(
            True, RepairEngine.GHOSTSCRIPT, "Ghostscript \u4fee\u5fa9\u6210\u529f", dst
        )
    return RepairResult(
        False, RepairEngine.GHOSTSCRIPT, f"Ghostscript \u5931\u6557: {result.stderr.strip()}"
    )


def _repair_with_copy(src: Path, dst: Path, password: str | None = None) -> RepairResult:
    """Last resort: simple file copy."""
    shutil.copy2(src, dst)
    return RepairResult(True, RepairEngine.SIMPLE_COPY, "\u7c21\u55ae\u8907\u88fd\u5b8c\u6210", dst)


def available_engines() -> list[RepairEngine]:
    """Detect which engines are importable / installed."""
    engines: list[RepairEngine] = []
    try:
        import fitz  # noqa: F401

        engines.append(RepairEngine.PYMUPDF)
    except ImportError:
        pass
    try:
        import PyPDF2  # noqa: F401

        engines.append(RepairEngine.PYPDF2)
    except ImportError:
        pass
    try:
        import pikepdf  # noqa: F401

        engines.append(RepairEngine.PIKEPDF)
    except ImportError:
        pass
    if _find_ghostscript():
        engines.append(RepairEngine.GHOSTSCRIPT)
    engines.append(RepairEngine.SIMPLE_COPY)
    return engines


_ENGINE_FUNCS = {
    RepairEngine.PYMUPDF: _repair_with_pymupdf,
    RepairEngine.PYPDF2: _repair_with_pypdf2,
    RepairEngine.PIKEPDF: _repair_with_pikepdf,
    RepairEngine.GHOSTSCRIPT: _repair_with_ghostscript,
    RepairEngine.SIMPLE_COPY: _repair_with_copy,
}


def repair_pdf(
    src: Path,
    dst: Path,
    password: str | None = None,
    engines: list[RepairEngine] | None = None,
    on_attempt: Callable[[str], None] | None = None,
) -> RepairResult:
    """
    Try each available engine in order until one succeeds.
    Returns the first successful result, or a failure result.
    """
    if engines is None:
        engines = available_engines()

    for engine in engines:
        func = _ENGINE_FUNCS.get(engine)
        if func is None:
            continue

        if on_attempt:
            on_attempt(engine.name)

        try:
            result = func(src, dst, password)
            if result.success and dst.exists() and dst.stat().st_size > 0:
                return result
        except Exception as exc:
            if on_attempt:
                on_attempt(f"{engine.name} \u5931\u6557: {exc}")
            continue

    return RepairResult(False, None, "\u6240\u6709\u4fee\u5fa9\u65b9\u6cd5\u90fd\u5931\u6557\u4e86")


def generate_output_path(src: Path, suffix: str = "_\u5df2\u4fee\u5fa9") -> Path:
    """Generate an output path with suffix, avoiding conflicts."""
    from pdf_toolbox.core.utils import ensure_unique_path

    output = src.parent / f"{src.stem}{suffix}{src.suffix}"
    return ensure_unique_path(output)
