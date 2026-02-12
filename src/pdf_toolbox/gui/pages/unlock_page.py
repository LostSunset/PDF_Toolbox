"""
PDF Unlock / Repair page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QRadioButton, QVBoxLayout

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.gui.widgets.password_dialog import PasswordDialog
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.unlock_worker import UnlockWorker


class UnlockPage(BasePage):
    """PDF unlock/repair page with auto and password modes."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f513 PDF \u89e3\u9396 / \u4fee\u5fa9",
            description=(
                "\u591a\u5f15\u64ce\u81ea\u52d5\u4fee\u5fa9\uff1a"
                "PyMuPDF \u2192 PyPDF2 \u2192 pikepdf \u2192 Ghostscript\u3002"
                "\u652f\u63f4\u5bc6\u78bc\u89e3\u9396\u548c\u7121\u5bc6\u78bc\u81ea\u52d5\u4fee\u5fa9\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        self._auto_radio = QRadioButton("\u81ea\u52d5\u4fee\u5fa9\uff08\u7121\u5bc6\u78bc\uff09")
        self._auto_radio.setChecked(True)
        self._pw_radio = QRadioButton("\u5bc6\u78bc\u89e3\u9396")
        group = QButtonGroup(self)
        group.addButton(self._auto_radio)
        group.addButton(self._pw_radio)
        row.addWidget(self._auto_radio)
        row.addWidget(self._pw_radio)
        row.addStretch()
        layout.addLayout(row)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        password = None
        if self._pw_radio.isChecked():
            password = PasswordDialog.get_password(self)
            if password is None:
                raise ValueError("\u5bc6\u78bc\u8f38\u5165\u5df2\u53d6\u6d88\u3002")
        return UnlockWorker(files, password=password)
