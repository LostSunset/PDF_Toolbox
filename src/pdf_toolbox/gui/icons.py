"""
Icon constants for sidebar navigation.
Using Unicode/emoji as placeholders; replace with SVG QIcon in production.
"""

from __future__ import annotations

import sys
from pathlib import Path


def get_app_icon_path() -> Path:
    """Resolve app icon path for both dev and PyInstaller bundled modes."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return base / "resources" / "icons" / "app.png"


# Sidebar page icons (icon_text, label)
PAGE_ICONS: list[tuple[str, str]] = [
    ("\U0001f3e0", "首頁"),
    ("\U0001f513", "解鎖 / 修復"),
    ("\U0001f5bc\ufe0f", "PDF 轉 PNG"),
    ("\U0001f512", "禁止複製"),
    ("\U0001f4ce", "合併"),
    ("\u2702\ufe0f", "拆分"),
    ("\U0001f504", "旋轉"),
    ("\U0001f4a7", "浮水印"),
    ("\U0001f4e6", "壓縮"),
    ("\u2195\ufe0f", "頁面重排序"),
]
