"""
PDF Split page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLineEdit,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
)

from pdf_toolbox.core.split import SplitMode
from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.split_worker import SplitWorker


class SplitPage(BasePage):
    """PDF split page with multiple split modes."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\u2702\ufe0f PDF \u62c6\u5206",
            description=(
                "\u6309\u9801\u78bc\u7bc4\u570d\u3001\u6bcf N \u9801"
                "\u6216\u63d0\u53d6\u7279\u5b9a\u9801\u9762\u4f86\u62c6\u5206 PDF\u3002"
            ),
            parent=parent,
        )

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        self._group = QButtonGroup(self)

        # By range
        row1 = QHBoxLayout()
        self._by_range = QRadioButton("\u6309\u9801\u78bc\u7bc4\u570d:")
        self._by_range.setChecked(True)
        self._group.addButton(self._by_range)
        row1.addWidget(self._by_range)
        self._range_input = QLineEdit()
        self._range_input.setPlaceholderText("\u4f8b: 1-3, 5, 7-10")
        row1.addWidget(self._range_input)
        layout.addLayout(row1)

        # Every N pages
        row2 = QHBoxLayout()
        self._every_n = QRadioButton("\u6bcf N \u9801\u62c6\u5206:")
        self._group.addButton(self._every_n)
        row2.addWidget(self._every_n)
        self._n_spin = QSpinBox()
        self._n_spin.setRange(1, 9999)
        self._n_spin.setValue(1)
        self._n_spin.setSuffix(" \u9801")
        row2.addWidget(self._n_spin)
        row2.addStretch()
        layout.addLayout(row2)

        # Extract specific pages
        row3 = QHBoxLayout()
        self._extract = QRadioButton("\u63d0\u53d6\u7279\u5b9a\u9801:")
        self._group.addButton(self._extract)
        row3.addWidget(self._extract)
        self._pages_input = QLineEdit()
        self._pages_input.setPlaceholderText("\u4f8b: 1, 3, 5")
        row3.addWidget(self._pages_input)
        layout.addLayout(row3)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        if self._by_range.isChecked():
            mode = SplitMode.BY_RANGE
        elif self._every_n.isChecked():
            mode = SplitMode.EVERY_N_PAGES
        else:
            mode = SplitMode.EXTRACT_PAGES

        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return SplitWorker(
            files,
            output_dir=out_dir,
            mode=mode,
            page_ranges=self._range_input.text(),
            pages_per_split=self._n_spin.value(),
            page_numbers_str=self._pages_input.text(),
        )
