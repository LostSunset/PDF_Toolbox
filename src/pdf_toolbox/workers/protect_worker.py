"""
Worker for PDF copy-protection.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.protect import generate_protected_path, protect_pdf
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult, TaskStatus

if TYPE_CHECKING:
    from collections.abc import Sequence


class ProtectWorker(BaseWorker):
    """Background worker for PDF copy-protection."""

    def __init__(
        self,
        files: Sequence[Path],
        output_dir: Path | None = None,
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._output_dir = output_dir

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        output_path = generate_protected_path(file_path, self._output_dir)
        result = protect_pdf(src=file_path, dst=output_path)
        return FileResult(
            source=file_path,
            output=output_path if result.success else None,
            status=TaskStatus.SUCCESS if result.success else TaskStatus.FAILED,
            message=(
                f"\u2713 {file_path.name} \u2192 {result.message}"
                if result.success
                else f"\u2717 {file_path.name} \u2192 {result.message}"
            ),
        )
