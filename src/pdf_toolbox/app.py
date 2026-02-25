"""Application bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication

from pdf_toolbox.gui.main_window import MainWindow
from pdf_toolbox.gui.theme import get_stylesheet


def _get_icon_path() -> Path:
    """Resolve app icon path for both dev and PyInstaller bundled modes."""
    # PyInstaller sets sys._MEIPASS for bundled apps
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / "resources" / "icons" / "app.png"


def main() -> None:
    """Launch the PDF Toolbox application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(get_stylesheet())
    app.setApplicationName("PDF Toolbox")

    # Application icon
    icon_path = _get_icon_path()
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Global default font
    font = QFont("Microsoft JhengHei", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
