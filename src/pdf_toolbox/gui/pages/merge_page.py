"""
PDF Merge page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QLabel, QVBoxLayout

from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.gui.widgets.file_list import FileListWidget
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.merge_worker import MergeWorker


class MergePage(BasePage):
    """PDF merge page with drag-reorder file list."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f4ce PDF \u5408\u4f75",
            description=(
                "\u5c07\u591a\u500b PDF \u6a94\u6848\u5408\u4f75\u70ba\u4e00\u500b\u3002"
                "\u53ef\u62d6\u653e\u6392\u5e8f\u6c7a\u5b9a\u5408\u4f75\u9806\u5e8f\u3002"
            ),
            parent=parent,
        )
        # Replace default FileListWidget with reorder-enabled one
        old_list = self.file_list
        layout = old_list.parent().layout()
        idx = layout.indexOf(old_list)
        old_list.setParent(None)
        old_list.deleteLater()
        self.file_list = FileListWidget(allow_reorder=True)
        layout.insertWidget(idx, self.file_list)
        self.drop_zone.files_dropped.connect(self._on_files_dropped_merge)

    def _on_files_dropped_merge(self, paths: list[str]) -> None:
        for p in paths:
            self.file_list.add_file(Path(p))

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        layout.addWidget(
            QLabel(
                "\u62d6\u653e\u4e0a\u65b9\u6a94\u6848\u5217\u8868\u4e2d\u7684\u9805\u76ee"
                "\u4f86\u8abf\u6574\u5408\u4f75\u9806\u5e8f\u3002"
            )
        )

    def create_worker(self, files: list[Path]) -> BaseWorker:
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        output_path = out_dir / "merged.pdf"
        from pdf_toolbox.core.utils import ensure_unique_path

        output_path = ensure_unique_path(output_path)
        return MergeWorker(files, output_path=output_path)
