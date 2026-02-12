"""Application bootstrap."""

from __future__ import annotations

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from pdf_toolbox.gui.main_window import MainWindow
from pdf_toolbox.gui.theme import get_stylesheet


def main() -> None:
    """Launch the PDF Toolbox application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(get_stylesheet())

    # Global default font
    font = QFont("Microsoft JhengHei", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
