"""
Worker for PDF merge (batch operation).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.merge import merge_pdfs
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult

if TYPE_CHECKING:
    from collections.abc import Sequence


class MergeWorker(BaseWorker):
    """Background worker for PDF merge. Overrides run() for batch operation."""

    def __init__(
        self,
        files: Sequence[Path],
        output_path: Path,
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._output_path = output_path

    def run(self) -> None:
        """Override: merge is a single-batch operation."""
        self.log_message.emit(f"\u6b63\u5728\u5408\u4f75 {len(self._files)} \u500b\u6a94\u6848...")
        self.progress_updated.emit(0, 1, "\u5408\u4f75\u4e2d...")

        try:
            result = merge_pdfs(self._files, self._output_path)
            self.progress_updated.emit(1, 1, result.message)
            self.log_message.emit(result.message)
            self.task_finished.emit(result.success, result.message, [])
        except Exception as exc:
            msg = f"\u5408\u4f75\u5931\u6557: {exc}"
            self.log_message.emit(msg)
            self.task_finished.emit(False, msg, [])

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        raise NotImplementedError("MergeWorker uses batch run().")
