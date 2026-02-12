"""
Worker for PDF split.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pdf_toolbox.core.split import SplitMode, split_pdf
from pdf_toolbox.workers.base_worker import BaseWorker, FileResult, TaskStatus

if TYPE_CHECKING:
    from collections.abc import Sequence


class SplitWorker(BaseWorker):
    """Background worker for PDF split."""

    def __init__(
        self,
        files: Sequence[Path],
        output_dir: Path,
        mode: SplitMode,
        page_ranges: str = "",
        pages_per_split: int = 1,
        page_numbers_str: str = "",
        parent: BaseWorker | None = None,
    ) -> None:
        super().__init__(files, parent)
        self._output_dir = output_dir
        self._mode = mode
        self._page_ranges = page_ranges
        self._pages_per_split = pages_per_split
        self._page_numbers_str = page_numbers_str

    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        page_numbers = None
        if self._mode == SplitMode.EXTRACT_PAGES and self._page_numbers_str:
            page_numbers = [
                int(x.strip()) - 1 for x in self._page_numbers_str.split(",") if x.strip().isdigit()
            ]

        result = split_pdf(
            src=file_path,
            output_dir=self._output_dir,
            mode=self._mode,
            page_ranges=self._page_ranges,
            pages_per_split=self._pages_per_split,
            page_numbers=page_numbers,
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
