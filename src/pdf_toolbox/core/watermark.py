"""
Add text or image watermark to PDF pages.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF


@dataclass
class WatermarkConfig:
    """Watermark parameters."""

    text: str = ""
    image_path: Path | None = None
    opacity: float = 0.3
    angle: float = -45.0
    position: str = "center"
    font_size: int = 48
    font_color: tuple[int, int, int] = (128, 128, 128)
    scale: float = 1.0


@dataclass
class WatermarkResult:
    """Result of a watermark operation."""

    success: bool
    message: str
    output_path: Path | None = None


def add_watermark(
    src: Path,
    dst: Path,
    config: WatermarkConfig,
    page_indices: list[int] | None = None,
) -> WatermarkResult:
    """
    Add a text or image watermark to PDF pages.
    Uses PyMuPDF for both text and image watermarks.
    """
    doc = fitz.open(str(src))
    try:
        total = len(doc)
        targets = page_indices if page_indices is not None else list(range(total))

        for idx in targets:
            if idx < 0 or idx >= total:
                continue
            page = doc[idx]

            if config.text:
                _add_text_watermark(page, config)
            elif config.image_path and config.image_path.exists():
                _add_image_watermark(page, config)

        doc.save(str(dst))
    finally:
        doc.close()

    return WatermarkResult(
        True,
        f"\u6d6e\u6c34\u5370\u65b0\u589e\u5b8c\u6210\uff01\u5171\u8655\u7406 {len(targets)} \u9801",
        dst,
    )


def _add_text_watermark(page: fitz.Page, config: WatermarkConfig) -> None:
    """Add text watermark to a single page."""
    rect = page.rect
    center = fitz.Point(rect.width / 2, rect.height / 2)

    # Create text writer
    r, g, b = config.font_color
    color = (r / 255, g / 255, b / 255)

    tw = fitz.TextWriter(page.rect)
    font = fitz.Font("helv")
    tw.append(
        center,
        config.text,
        font=font,
        fontsize=config.font_size,
    )

    # Apply with rotation and opacity
    page.insert_text(
        center,
        config.text,
        fontsize=config.font_size,
        fontname="helv",
        color=color,
        rotate=int(config.angle),
        overlay=True,
        stroke_opacity=config.opacity,
        fill_opacity=config.opacity,
    )


def _add_image_watermark(page: fitz.Page, config: WatermarkConfig) -> None:
    """Add image watermark to a single page."""
    rect = page.rect
    img_rect = fitz.Rect(rect)

    # Scale the image
    if config.scale != 1.0:
        w = rect.width * config.scale
        h = rect.height * config.scale
        x = (rect.width - w) / 2
        y = (rect.height - h) / 2
        img_rect = fitz.Rect(x, y, x + w, y + h)

    page.insert_image(
        img_rect,
        filename=str(config.image_path),
        overlay=True,
        alpha=int(config.opacity * 255),
        rotate=int(config.angle),
    )
