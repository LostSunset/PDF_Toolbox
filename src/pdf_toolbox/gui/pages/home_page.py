"""
Home / welcome page for PDF Toolbox.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from pdf_toolbox import __version__
from pdf_toolbox.gui.theme import PALETTE


class HomePage(QWidget):
    """Welcome page displayed when the app starts."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # App title
        title = QLabel("PDF Toolbox")
        title.setFont(QFont("Microsoft JhengHei", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {PALETTE.blue};")
        layout.addWidget(title)

        # Version
        version_label = QLabel(f"v{__version__}")
        version_label.setFont(QFont("Microsoft JhengHei", 14))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: {PALETTE.overlay1};")
        layout.addWidget(version_label)

        # Description
        desc = QLabel("統一的 PDF 處理工具箱")
        desc.setFont(QFont("Microsoft JhengHei", 16))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"color: {PALETTE.subtext1};")
        layout.addWidget(desc)

        # Feature list
        features = [
            "解鎖 / 修復 — 多引擎自動修復受損或加密的 PDF",
            "PDF 轉 PNG — 高解析度 PDF 頁面轉換",
            "禁止複製 — 為 PDF 設定複製保護",
            "合併 — 將多個 PDF 合併為一個",
            "拆分 — 按頁碼範圍拆分 PDF",
            "旋轉 — 旋轉 PDF 頁面",
            "浮水印 — 添加文字或圖片浮水印",
            "壓縮 — 縮小 PDF 檔案大小",
            "頁面重排序 — 調整頁面順序",
        ]

        feature_text = "\n".join(f"  \u2022  {f}" for f in features)
        feature_label = QLabel(feature_text)
        feature_label.setFont(QFont("Microsoft JhengHei", 12))
        feature_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        feature_label.setStyleSheet(
            f"color: {PALETTE.subtext0}; "
            f"background-color: {PALETTE.surface0}; "
            f"border-radius: 10px; "
            f"padding: 20px 30px;"
        )
        layout.addWidget(feature_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Hint
        hint = QLabel("從左側選單選擇工具開始使用")
        hint.setFont(QFont("Microsoft JhengHei", 11))
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet(f"color: {PALETTE.overlay0};")
        layout.addWidget(hint)
