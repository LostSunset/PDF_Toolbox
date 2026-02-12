"""
PDF Page Reorder page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.gui.theme import PALETTE
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.reorder_worker import ReorderWorker


class ReorderPage(BasePage):
    """PDF page reorder page."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\u2195\ufe0f \u9801\u9762\u91cd\u6392\u5e8f",
            description=(
                "\u8abf\u6574 PDF \u9801\u9762\u9806\u5e8f\u3002"
                "\u8f38\u5165\u65b0\u7684\u9801\u78bc\u9806\u5e8f\u4f86\u91cd\u65b0\u6392\u5217\u9801\u9762\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.addWidget(QLabel("\u65b0\u9806\u5e8f:"))
        self._order_input = QLineEdit()
        self._order_input.setPlaceholderText(
            "\u4f8b: 3,1,2,5,4 (\u5c07\u7b2c3\u9801\u653e\u6700\u524d)"
        )
        row.addWidget(self._order_input)

        self._reverse_btn = QPushButton("\u53cd\u8f49\u9806\u5e8f")
        self._reverse_btn.clicked.connect(self._fill_reverse)
        row.addWidget(self._reverse_btn)
        layout.addLayout(row)

        info = QLabel(
            "\u2139\ufe0f \u8f38\u5165\u4ee5\u9017\u865f\u5206\u9694\u7684\u9801\u78bc"
            '\uff0c\u4f8b\u5982 "3,1,2" \u8868\u793a\u7b2c3\u9801\u5728\u524d'
            "\u3001\u7b2c1\u9801\u5728\u4e2d\u3001\u7b2c2\u9801\u5728\u5f8c"
        )
        info.setStyleSheet(f"color: {PALETTE.subtext0}; padding: 4px;")
        info.setWordWrap(True)
        layout.addWidget(info)

    def _fill_reverse(self) -> None:
        """Fill input with reverse order based on first selected file."""
        files = self.file_list.get_all_files()
        if not files:
            QMessageBox.warning(
                self, "\u8b66\u544a", "\u8acb\u5148\u65b0\u589e PDF \u6a94\u6848\u3002"
            )
            return
        from pdf_toolbox.core.reorder import get_page_count

        try:
            count = get_page_count(files[0])
            reverse_order = ",".join(str(i) for i in range(count, 0, -1))
            self._order_input.setText(reverse_order)
        except Exception as exc:
            QMessageBox.warning(self, "\u932f\u8aa4", str(exc))

    def validate_before_start(self) -> str | None:
        error = super().validate_before_start()
        if error:
            return error
        if not self._order_input.text().strip():
            return "\u8acb\u8f38\u5165\u65b0\u7684\u9801\u9762\u9806\u5e8f\u3002"
        return None

    def create_worker(self, files: list[Path]) -> BaseWorker:
        order_text = self._order_input.text().strip()
        new_order = [int(x.strip()) - 1 for x in order_text.split(",") if x.strip().isdigit()]
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return ReorderWorker(files, new_order=new_order, output_dir=out_dir)
