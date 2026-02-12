"""
Worker for PDF unlock/repair.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.unlock import generate_output_path, repair_pdf
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult, TaskStatus

if TYPE_CHECKING:
    from collections.abc import Sequence


class UnlockWorker(BaseWorker):
    """Background worker for PDF unlock/repair."""

    def __init__(
        self,
        files: Sequence[Path],
        password: str | None = None,
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._password = password

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        output_path = generate_output_path(file_path)
        result = repair_pdf(
            src=file_path,
            dst=output_path,
            password=self._password,
            on_attempt=lambda name: self.log_message.emit(f"  \u5617\u8a66 {name}..."),
        )
        return FileResult(
            source=file_path,
            output=output_path if result.success else None,
            status=TaskStatus.SUCCESS if result.success else TaskStatus.FAILED,
            message=(
                f"\u2713 {file_path.name} \u2192 {result.message}"
                if result.success
                else f"\u2717 {file_path.name} \u2192 {result.message}"
            ),
            engine=result.engine.name if result.engine else "",
        )
