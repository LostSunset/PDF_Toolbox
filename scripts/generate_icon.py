"""Generate PDF Toolbox application icon (ICO with multiple sizes)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Catppuccin Mocha palette
RED = (243, 139, 168)  # #f38ba8
BLUE = (137, 180, 250)  # #89b4fa
DARK = (30, 30, 46)  # #1e1e2e (base)
CRUST = (17, 17, 27)  # #11111b
WHITE = (205, 214, 244)  # #cdd6f4 (text)
SURFACE0 = (49, 50, 68)  # #313244

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "src" / "pdf_toolbox" / "resources" / "icons"


def draw_rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, ...],
) -> None:
    """Draw a rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_document(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw a document shape with folded corner."""
    margin = int(size * 0.12)
    fold = int(size * 0.2)
    doc_x0 = margin
    doc_y0 = margin
    doc_x1 = size - margin
    doc_y1 = size - margin

    # Document body (white-ish)
    body_color = (235, 235, 245)
    points = [
        (doc_x0, doc_y0),
        (doc_x1 - fold, doc_y0),
        (doc_x1, doc_y0 + fold),
        (doc_x1, doc_y1),
        (doc_x0, doc_y1),
    ]
    draw.polygon(points, fill=body_color)

    # Folded corner
    fold_color = (200, 200, 215)
    fold_points = [
        (doc_x1 - fold, doc_y0),
        (doc_x1, doc_y0 + fold),
        (doc_x1 - fold, doc_y0 + fold),
    ]
    draw.polygon(fold_points, fill=fold_color)


def draw_pdf_badge(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw the 'PDF' badge at the bottom of the document."""
    badge_h = int(size * 0.22)
    badge_y = size - int(size * 0.12) - badge_h
    badge_x0 = int(size * 0.12)
    badge_x1 = size - int(size * 0.12)
    radius = int(size * 0.04)

    draw_rounded_rect(draw, (badge_x0, badge_y, badge_x1, badge_y + badge_h), radius, RED)

    # "PDF" text
    font_size = int(badge_h * 0.65)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    text = "PDF"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = badge_x0 + (badge_x1 - badge_x0 - tw) // 2
    ty = badge_y + (badge_h - th) // 2 - int(badge_h * 0.08)
    draw.text((tx, ty), text, fill=WHITE, font=font)


def draw_wrench(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw a small wrench/gear symbol in the top-right area of the document."""
    cx = int(size * 0.62)
    cy = int(size * 0.38)
    r = int(size * 0.12)

    # Gear: outer circle with teeth
    teeth = 6
    outer_r = r
    tooth_size = int(r * 0.25)

    # Draw gear teeth
    for i in range(teeth):
        angle = (2 * math.pi * i) / teeth
        tx = cx + int((outer_r + tooth_size * 0.3) * math.cos(angle))
        ty = cy + int((outer_r + tooth_size * 0.3) * math.sin(angle))
        draw.ellipse(
            (tx - tooth_size, ty - tooth_size, tx + tooth_size, ty + tooth_size),
            fill=BLUE,
        )

    # Gear body
    draw.ellipse((cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r), fill=BLUE)

    # Gear hole
    hole_r = int(r * 0.35)
    draw.ellipse((cx - hole_r, cy - hole_r, cx + hole_r, cy + hole_r), fill=(235, 235, 245))


def draw_lines(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Draw document lines (subtle detail)."""
    margin = int(size * 0.12)
    line_x0 = margin + int(size * 0.08)
    line_x1 = int(size * 0.5)
    line_color = (190, 190, 205)
    line_h = int(size * 0.015)
    if line_h < 1:
        line_h = 1

    for i, y_frac in enumerate([0.3, 0.38, 0.46]):
        y = int(size * y_frac)
        x1 = line_x1 if i < 2 else int(line_x1 * 0.8)
        draw.rounded_rectangle(
            (line_x0, y, x1, y + line_h),
            radius=line_h,
            fill=line_color,
        )


def generate_icon(size: int) -> Image.Image:
    """Generate a single icon at the given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background rounded rectangle
    bg_radius = int(size * 0.18)
    draw_rounded_rect(draw, (0, 0, size - 1, size - 1), bg_radius, DARK)

    # Document shape
    draw_document(draw, size)

    # Document lines
    draw_lines(draw, size)

    # Gear/wrench symbol
    if size >= 48:
        draw_wrench(draw, size)

    # PDF badge
    draw_pdf_badge(draw, size)

    return img


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate multiple sizes for ICO
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []
    for s in sizes:
        img = generate_icon(s)
        images.append(img)

    # Save as ICO (multi-size)
    ico_path = OUTPUT_DIR / "app.ico"
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print(f"Generated: {ico_path}")

    # Also save a 256px PNG for use in Qt
    png_path = OUTPUT_DIR / "app.png"
    images[-1].save(png_path, format="PNG")
    print(f"Generated: {png_path}")

    # Save a 512px PNG for higher resolution displays
    img_512 = generate_icon(512)
    png_512_path = OUTPUT_DIR / "app_512.png"
    img_512.save(png_512_path, format="PNG")
    print(f"Generated: {png_512_path}")


if __name__ == "__main__":
    main()
