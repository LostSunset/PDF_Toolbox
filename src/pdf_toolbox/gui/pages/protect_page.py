"""
PDF copy-protection page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QLabel, QVBoxLayout

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.gui.theme import PALETTE
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.protect_worker import ProtectWorker


class ProtectPage(BasePage):
    """PDF copy-protection page."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f512 PDF \u7981\u6b62\u8907\u88fd\u4fdd\u8b77",
            description=(
                "\u4f7f\u7528 pikepdf + PyPDF2 \u96d9\u5c64\u52a0\u5bc6\uff0c"
                "\u7981\u6b62\u8907\u88fd\u6587\u5b57\u4f46\u5141\u8a31\u5217\u5370\u3002"
                "\u8f38\u51fa\u6a94\u6848\u540d\u6703\u52a0\u4e0a _p \u5f8c\u7db4\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        info = QLabel(
            "\u2139\ufe0f \u4fdd\u8b77\u6a21\u5f0f\uff1a"
            "\u7981\u6b62\u8907\u88fd / \u64f7\u53d6\u6587\u5b57\uff0c"
            "\u5141\u8a31\u5217\u5370"
        )
        info.setStyleSheet(f"color: {PALETTE.yellow}; padding: 8px;")
        layout.addWidget(info)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return ProtectWorker(files, output_dir=out_dir)
