"""Generate PDF Toolbox application icon (ICO with multiple sizes)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Catppuccin Mocha palette
RED = (243, 139, 168)  # #f38ba8
BLUE = (137, 180, 250)  # #89b4fa
DARK = (30, 30, 46)  # #1e1e2e (base)
WHITE = (205, 214, 244)  # #cdd6f4 (text)

# Document colors
DOC_BODY = (235, 235, 245)
DOC_FOLD = (200, 200, 215)
DOC_LINE = (190, 190, 205)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "src" / "pdf_toolbox" / "resources" / "icons"

# Margin ratio - keep content well inside the rounded background
MARGIN = 0.20
BG_RADIUS = 0.22


def _s(size: int, ratio: float) -> int:
    """Scale a ratio to pixel size."""
    return int(size * ratio)


def draw_document(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw a document shape with folded corner."""
    m = _s(size, MARGIN)
    fold = _s(size, 0.16)
    x0, y0, x1, y1 = m, m, size - m, size - m
    doc_r = _s(size, 0.04)

    # Main document body (rounded rect, then overlay fold)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=doc_r, fill=DOC_BODY)

    # Cut the top-right corner for the fold: draw dark triangle to "remove" it,
    # then draw the fold triangle on top
    # Triangle to mask top-right corner with background color
    mask_points = [
        (x1 - fold, y0 - 1),
        (x1 + 1, y0 - 1),
        (x1 + 1, y0 + fold),
    ]
    draw.polygon(mask_points, fill=DARK)

    # Diagonal edge (document body visible part)
    edge_points = [
        (x1 - fold, y0),
        (x1, y0 + fold),
        (x1, y1 - doc_r),
        (x1, y1),
        (x0, y1),
        (x0, y0),
        (x1 - fold, y0),
    ]
    draw.polygon(edge_points, fill=DOC_BODY)

    # Folded corner triangle
    fold_points = [
        (x1 - fold, y0),
        (x1, y0 + fold),
        (x1 - fold, y0 + fold),
    ]
    draw.polygon(fold_points, fill=DOC_FOLD)


def draw_lines(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw document text lines."""
    m = _s(size, MARGIN)
    line_x0 = m + _s(size, 0.07)
    line_h = max(_s(size, 0.018), 1)

    for i, y_frac in enumerate([0.35, 0.43, 0.51]):
        y = _s(size, y_frac)
        x1 = _s(size, 0.48) if i < 2 else _s(size, 0.40)
        draw.rounded_rectangle((line_x0, y, x1, y + line_h), radius=line_h, fill=DOC_LINE)


def draw_gear(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw a gear symbol on the document."""
    cx = _s(size, 0.60)
    cy = _s(size, 0.42)
    r = _s(size, 0.10)
    teeth = 6
    tooth_r = max(_s(size, 0.028), 2)

    # Gear teeth
    for i in range(teeth):
        angle = (2 * math.pi * i) / teeth
        tx = cx + int((r + tooth_r * 0.4) * math.cos(angle))
        ty = cy + int((r + tooth_r * 0.4) * math.sin(angle))
        draw.ellipse((tx - tooth_r, ty - tooth_r, tx + tooth_r, ty + tooth_r), fill=BLUE)

    # Gear body
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BLUE)

    # Gear hole
    hole_r = max(_s(size, 0.035), 2)
    draw.ellipse((cx - hole_r, cy - hole_r, cx + hole_r, cy + hole_r), fill=DOC_BODY)


def draw_pdf_badge(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw the 'PDF' badge at the bottom of the document."""
    m = _s(size, MARGIN)
    badge_h = _s(size, 0.18)
    badge_x0 = m + _s(size, 0.02)
    badge_x1 = size - m - _s(size, 0.02)
    badge_y1 = size - m - _s(size, 0.04)
    badge_y0 = badge_y1 - badge_h
    radius = _s(size, 0.03)

    draw.rounded_rectangle((badge_x0, badge_y0, badge_x1, badge_y1), radius=radius, fill=RED)

    # "PDF" text
    font_size = int(badge_h * 0.7)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
            except OSError:
                font = ImageFont.load_default()

    text = "PDF"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = badge_x0 + (badge_x1 - badge_x0 - tw) // 2
    ty = badge_y0 + (badge_h - th) // 2 - int(badge_h * 0.08)
    draw.text((tx, ty), text, fill=WHITE, font=font)


def generate_icon(size: int) -> Image.Image:
    """Generate a single icon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    bg_r = _s(size, BG_RADIUS)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=bg_r, fill=DARK)

    # Document
    draw_document(draw, size)

    # Text lines
    draw_lines(draw, size)

    # Gear symbol (skip for tiny sizes)
    if size >= 48:
        draw_gear(draw, size)

    # PDF badge
    draw_pdf_badge(draw, size)

    return img


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Multi-size ICO
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = [generate_icon(s) for s in sizes]

    ico_path = OUTPUT_DIR / "app.ico"
    images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
    print(f"Generated: {ico_path}")

    # 256px PNG for Qt window icon
    png_path = OUTPUT_DIR / "app.png"
    images[-1].save(png_path, format="PNG")
    print(f"Generated: {png_path}")

    # 512px PNG for README / high-DPI
    img_512 = generate_icon(512)
    png_512_path = OUTPUT_DIR / "app_512.png"
    img_512.save(png_512_path, format="PNG")
    print(f"Generated: {png_512_path}")


if __name__ == "__main__":
    main()
