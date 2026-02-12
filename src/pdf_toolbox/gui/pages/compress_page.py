"""
PDF Compress page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout

from pdf_toolbox.core.compress import CompressionLevel
from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.gui.theme import PALETTE
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.compress_worker import CompressWorker

_LEVELS = [
    ("\u4f4e\u58d3\u7e2e (\u6700\u9ad8\u54c1\u8cea)", CompressionLevel.LOW),
    ("\u4e2d\u7b49\u58d3\u7e2e (\u5e73\u8861)", CompressionLevel.MEDIUM),
    ("\u9ad8\u58d3\u7e2e (\u8f03\u5c0f\u6a94\u6848)", CompressionLevel.HIGH),
    ("\u6700\u5927\u58d3\u7e2e (\u6700\u5c0f\u6a94\u6848)", CompressionLevel.MAXIMUM),
]


class CompressPage(BasePage):
    """PDF compression page."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f4e6 PDF \u58d3\u7e2e",
            description=(
                "\u7e2e\u5c0f PDF \u6a94\u6848\u5927\u5c0f\u3002"
                "\u4f7f\u7528 Ghostscript \u6216 PyMuPDF \u9032\u884c\u58d3\u7e2e\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.addWidget(QLabel("\u58d3\u7e2e\u7b49\u7d1a:"))
        self._level_combo = QComboBox()
        for label, _ in _LEVELS:
            self._level_combo.addItem(label)
        self._level_combo.setCurrentIndex(1)  # Default to MEDIUM
        row.addWidget(self._level_combo)
        row.addStretch()
        layout.addLayout(row)

        info = QLabel(
            "\u2139\ufe0f \u58d3\u7e2e\u7b49\u7d1a\u8d8a\u9ad8\uff0c"
            "\u6a94\u6848\u8d8a\u5c0f\u4f46\u5716\u7247\u54c1\u8cea\u53ef\u80fd\u964d\u4f4e"
        )
        info.setStyleSheet(f"color: {PALETTE.yellow}; padding: 4px;")
        layout.addWidget(info)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        _, level = _LEVELS[self._level_combo.currentIndex()]
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return CompressWorker(files, level=level, output_dir=out_dir)
