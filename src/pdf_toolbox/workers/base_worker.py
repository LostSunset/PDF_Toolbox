"""
Base worker class providing unified progress reporting and cancellation.
"""

from __future__ import annotations

import traceback
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QThread, Signal

if TYPE_CHECKING:
    from collections.abc import Sequence


class TaskStatus(Enum):
    """Status of a single file operation."""

    SUCCESS = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class FileResult:
    """Result for a single file operation."""

    source: Path
    output: Path | None
    status: TaskStatus
    message: str
    engine: str = ""


class BaseWorker(QThread):
    """
    Abstract base for all background workers.

    Signals (unified across all workers):
        progress_updated(current: int, total: int, message: str)
        file_completed(source_name: str, success: bool, message: str)
        log_message(message: str)
        task_finished(success: bool, summary: str, results: list)
    """

    progress_updated = Signal(int, int, str)
    file_completed = Signal(str, bool, str)
    log_message = Signal(str)
    task_finished = Signal(bool, str, list)

    def __init__(self, files: Sequence[Path], parent: QThread | None = None) -> None:
        super().__init__(parent)
        self._files: list[Path] = list(files)
        self._is_cancelled: bool = False
        self._results: list[FileResult] = []

    def cancel(self) -> None:
        """Request cancellation."""
        self._is_cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

    @property
    def results(self) -> list[FileResult]:
        return list(self._results)

    def run(self) -> None:
        """Template method: iterates files and calls process_file for each."""
        total = len(self._files)
        if total == 0:
            self.task_finished.emit(
                False, "\u6c92\u6709\u6a94\u6848\u9700\u8981\u8655\u7406\u3002", []
            )
            return

        self.log_message.emit(
            f"\u958b\u59cb\u8655\u7406\uff0c\u5171 {total} \u500b\u6a94\u6848\u3002"
        )
        success_count = 0

        try:
            for i, file_path in enumerate(self._files):
                if self._is_cancelled:
                    self.log_message.emit("\u4f7f\u7528\u8005\u5df2\u53d6\u6d88\u64cd\u4f5c\u3002")
                    break

                self.progress_updated.emit(i + 1, total, f"\u8655\u7406\u4e2d: {file_path.name}")

                try:
                    result = self.process_file(file_path, i, total)
                    self._results.append(result)

                    ok = result.status == TaskStatus.SUCCESS
                    if ok:
                        success_count += 1
                    self.file_completed.emit(file_path.name, ok, result.message)
                    self.log_message.emit(result.message)

                except Exception as exc:
                    msg = f"\u8655\u7406 {file_path.name} \u6642\u767c\u751f\u932f\u8aa4: {exc}"
                    self.log_message.emit(msg)
                    self.log_message.emit(traceback.format_exc())
                    self._results.append(
                        FileResult(
                            source=file_path,
                            output=None,
                            status=TaskStatus.FAILED,
                            message=msg,
                        )
                    )
                    self.file_completed.emit(file_path.name, False, msg)

        except Exception as exc:
            self.log_message.emit(f"\u56b4\u91cd\u932f\u8aa4: {exc}")
            self.task_finished.emit(False, f"\u56b4\u91cd\u932f\u8aa4: {exc}", self._results)
            return

        if self._is_cancelled:
            summary = (
                f"\u5df2\u53d6\u6d88\u3002\u53d6\u6d88\u524d\u5b8c\u6210 "
                f"{success_count}/{total} \u500b\u6a94\u6848\u3002"
            )
            self.task_finished.emit(False, summary, self._results)
        else:
            summary = (
                f"\u5b8c\u6210\uff01\u6210\u529f {success_count}/{total} \u500b\u6a94\u6848\u3002"
            )
            self.task_finished.emit(success_count > 0, summary, self._results)

    @abstractmethod
    def process_file(self, file_path: Path, index: int, total: int) -> FileResult:
        """
        Process a single file. Must be implemented by each worker subclass.
        Should NOT catch exceptions -- the base class handles that.
        """
        ...
