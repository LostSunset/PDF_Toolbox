"""
PDF to PNG conversion page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.convert_worker import ConvertWorker


class ConvertPage(BasePage):
    """PDF to PNG conversion page with DPI settings."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f5bc\ufe0f PDF \u8f49 PNG",
            description=(
                "\u4f7f\u7528 pdftoppm \u5c07 PDF \u9801\u9762\u8f49\u63db\u70ba"
                "\u9ad8\u89e3\u6790\u5ea6 PNG \u5716\u7247\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.addWidget(QLabel("DPI:"))
        self._dpi_spin = QSpinBox()
        self._dpi_spin.setRange(72, 2400)
        self._dpi_spin.setValue(1200)
        self._dpi_spin.setSuffix(" dpi")
        self._dpi_spin.setToolTip(
            "\u8f03\u9ad8\u7684 DPI \u7522\u751f\u66f4\u9ad8\u89e3\u6790\u5ea6\u7684\u5716\u7247"
            "\uff0c\u4f46\u6a94\u6848\u66f4\u5927"
        )
        row.addWidget(self._dpi_spin)

        row.addStretch()
        row.addWidget(QLabel("\u9810\u8a2d:"))

        for dpi in (150, 300, 600, 1200):
            btn = QPushButton(str(dpi))
            btn.setFixedWidth(55)
            btn.clicked.connect(lambda _, d=dpi: self._dpi_spin.setValue(d))
            row.addWidget(btn)

        layout.addLayout(row)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return ConvertWorker(files, dpi=self._dpi_spin.value(), output_dir=out_dir)
