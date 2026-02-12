"""
Main application window with sidebar navigation and stacked pages.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pdf_toolbox import __version__
from pdf_toolbox.gui.icons import PAGE_ICONS
from pdf_toolbox.gui.theme import PALETTE, get_sidebar_stylesheet, get_stylesheet


class Sidebar(QFrame):
    """Left sidebar navigation panel."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(200)
        self.setStyleSheet(get_sidebar_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App title
        title = QLabel("PDF Toolbox")
        title.setFont(QFont("Microsoft JhengHei", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"color: {PALETTE.blue}; padding: 20px 0; background-color: {PALETTE.crust};"
        )
        layout.addWidget(title)

        # Navigation buttons
        self._buttons: list[QPushButton] = []
        for icon_text, label in PAGE_ICONS:
            btn = QPushButton(f"  {icon_text}  {label}")
            btn.setProperty("class", "sidebar-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(44)
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addStretch()

        # Version label
        ver_label = QLabel(f"v{__version__}")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver_label.setStyleSheet(f"color: {PALETTE.overlay0}; padding: 10px;")
        layout.addWidget(ver_label)

    def connect_button(self, index: int, callback: object) -> None:
        """Connect a sidebar button click to a callback."""
        self._buttons[index].clicked.connect(callback)

    def set_active(self, index: int) -> None:
        """Highlight the active button."""
        for i, btn in enumerate(self._buttons):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)


class MainWindow(QMainWindow):
    """Application main window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF Toolbox")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(get_stylesheet())
        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Stacked pages
        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked, 1)

        # Register pages
        self._pages: list[QWidget] = []
        self._register_pages()

        # Connect sidebar buttons
        for i in range(len(self._pages)):
            self.sidebar.connect_button(i, lambda checked=False, idx=i: self._switch_page(idx))

        # Default to home page
        self._switch_page(0)

    def _register_pages(self) -> None:
        """Register all feature pages."""
        from pdf_toolbox.gui.pages.compress_page import CompressPage
        from pdf_toolbox.gui.pages.convert_page import ConvertPage
        from pdf_toolbox.gui.pages.home_page import HomePage
        from pdf_toolbox.gui.pages.merge_page import MergePage
        from pdf_toolbox.gui.pages.protect_page import ProtectPage
        from pdf_toolbox.gui.pages.reorder_page import ReorderPage
        from pdf_toolbox.gui.pages.rotate_page import RotatePage
        from pdf_toolbox.gui.pages.split_page import SplitPage
        from pdf_toolbox.gui.pages.unlock_page import UnlockPage
        from pdf_toolbox.gui.pages.watermark_page import WatermarkPage

        page_classes: list[type[QWidget]] = [
            HomePage,  # 0: Home
            UnlockPage,  # 1: Unlock
            ConvertPage,  # 2: Convert
            ProtectPage,  # 3: Protect
            MergePage,  # 4: Merge
            SplitPage,  # 5: Split
            RotatePage,  # 6: Rotate
            WatermarkPage,  # 7: Watermark
            CompressPage,  # 8: Compress
            ReorderPage,  # 9: Reorder
        ]

        for page_cls in page_classes:
            page = page_cls()
            self._pages.append(page)
            self.stacked.addWidget(page)

    def _switch_page(self, index: int) -> None:
        """Switch to the page at the given index."""
        self.stacked.setCurrentIndex(index)
        self.sidebar.set_active(index)
