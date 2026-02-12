"""
Worker for PDF rotation.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.rotate import rotate_pdf
from pdf_toolbox.core.utils import ensure_unique_path
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult, TaskStatus

if TYPE_CHECKING:
    from collections.abc import Sequence


class RotateWorker(BaseWorker):
    """Background worker for PDF rotation."""

    def __init__(
        self,
        files: Sequence[Path],
        degrees: int = 90,
        page_indices: list[int] | None = None,
        output_dir: Path | None = None,
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._degrees = degrees
        self._page_indices = page_indices
        self._output_dir = output_dir

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        parent = self._output_dir or file_path.parent
        output_path = ensure_unique_path(parent / f"{file_path.stem}_rotated{file_path.suffix}")
        result = rotate_pdf(
            src=file_path,
            dst=output_path,
            degrees=self._degrees,
            page_indices=self._page_indices,
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
        )
