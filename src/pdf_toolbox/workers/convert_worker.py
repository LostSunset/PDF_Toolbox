"""
Worker for PDF to PNG conversion.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.convert import convert_pdf_to_png
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult, TaskStatus

if TYPE_CHECKING:
    from collections.abc import Sequence


class ConvertWorker(BaseWorker):
    """Background worker for PDF to PNG conversion."""

    def __init__(
        self,
        files: Sequence[Path],
        dpi: int = 1200,
        output_dir: Path | None = None,
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._dpi = dpi
        self._output_dir = output_dir

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        result = convert_pdf_to_png(
            file_path,
            output_dir=self._output_dir,
            dpi=self._dpi,
        )
        return FileResult(
            source=file_path,
            output=result.output_files[0] if result.output_files else None,
            status=TaskStatus.SUCCESS if result.success else TaskStatus.FAILED,
            message=(
                f"\u2713 {file_path.name} \u2192 {result.message}"
                if result.success
                else f"\u2717 {file_path.name} \u2192 {result.message}"
            ),
        )
