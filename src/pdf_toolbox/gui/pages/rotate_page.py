"""
PDF Rotate page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.rotate_worker import RotateWorker


class RotatePage(BasePage):
    """PDF rotation page."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f504 PDF \u65cb\u8f49",
            description="\u65cb\u8f49 PDF \u9801\u9762 90\u00b0\u3001180\u00b0 \u6216 270\u00b0\u3002",
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.addWidget(QLabel("\u65cb\u8f49\u89d2\u5ea6:"))
        self._degrees_combo = QComboBox()
        self._degrees_combo.addItems(["90\u00b0", "180\u00b0", "270\u00b0"])
        row.addWidget(self._degrees_combo)

        row.addWidget(QLabel("\u9801\u9762:"))
        self._pages_input = QLineEdit()
        self._pages_input.setPlaceholderText(
            "\u5168\u90e8 (\u6216\u6307\u5b9a\u9801\u78bc\uff0c\u4f8b: 1,3,5)"
        )
        row.addWidget(self._pages_input)
        row.addStretch()
        layout.addLayout(row)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        degrees_text = self._degrees_combo.currentText().replace("\u00b0", "")
        degrees = int(degrees_text)

        pages_str = self._pages_input.text().strip()
        page_indices = None
        if pages_str:
            page_indices = [int(x.strip()) - 1 for x in pages_str.split(",") if x.strip().isdigit()]

        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return RotateWorker(files, degrees=degrees, page_indices=page_indices, output_dir=out_dir)
