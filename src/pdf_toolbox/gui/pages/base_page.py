"""
Base page providing shared layout scaffolding for all feature pages.
"""

from __future__ import annotations

from abc import abstractmethod
from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from pdf_toolbox.gui.theme import PALETTE
from pdf_toolbox.gui.widgets.drop_zone import DropZone
from pdf_toolbox.gui.widgets.file_list import FileListWidget
from pdf_toolbox.gui.widgets.log_panel import LogPanel
from pdf_toolbox.gui.widgets.output_dir_selector import OutputDirSelector
from pdf_toolbox.gui.widgets.progress_panel import ProgressPanel
from pdf_toolbox.workers.base_worker import BaseWorker


class BasePage(QWidget):
    """
    Standard layout for a feature page:
      [Title + Description]
      [DropZone]
      [FileList]
      [Settings area]      <-- build_settings_area()
      [OutputDirSelector]
      [ProgressPanel]
      [LogPanel]
      [Start / Cancel]
    """

    def __init__(
        self,
        title: str,
        description: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._title_text = title
        self._description_text = description
        self._worker: BaseWorker | None = None
        self._setup_layout()

    def _setup_layout(self) -> None:
        # Wrap content in scroll area for small screens
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        outer_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        # Title
        title_label = QLabel(self._title_text)
        title_label.setFont(QFont("Microsoft JhengHei", 18, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {PALETTE.text};")
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(self._description_text)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: {PALETTE.subtext0};")
        layout.addWidget(desc_label)

        # Drop zone
        self.drop_zone = DropZone(accepted_extensions=[".pdf"])
        self.drop_zone.files_dropped.connect(self._on_files_dropped)
        layout.addWidget(self.drop_zone)

        # File list
        self.file_list = FileListWidget()
        layout.addWidget(self.file_list)

        # Settings area (subclass fills this)
        self._settings_container = QWidget()
        self._settings_layout = QVBoxLayout(self._settings_container)
        self._settings_layout.setContentsMargins(0, 0, 0, 0)
        self.build_settings_area(self._settings_layout)
        layout.addWidget(self._settings_container)

        # Output directory
        self.output_dir_selector = OutputDirSelector()
        layout.addWidget(self.output_dir_selector)

        # Progress
        self.progress_panel = ProgressPanel()
        layout.addWidget(self.progress_panel)

        # Log
        self.log_panel = LogPanel()
        layout.addWidget(self.log_panel)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.start_btn = self._make_button("\U0001f680 \u958b\u59cb\u8655\u7406", "primary")
        self.start_btn.clicked.connect(self._on_start_clicked)
        self.cancel_btn = self._make_button("\u274c \u53d6\u6d88", "danger")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._on_cancel_clicked)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    # -- Override points --

    @abstractmethod
    def build_settings_area(self, layout: QVBoxLayout) -> None:
        """Add page-specific settings widgets to the given layout."""
        ...

    @abstractmethod
    def create_worker(self, files: list[Path]) -> BaseWorker:
        """Create and return the appropriate worker for this page."""
        ...

    def validate_before_start(self) -> str | None:
        """Return an error message if validation fails, or None if OK."""
        if self.file_list.count() == 0:
            return "\u8acb\u5148\u65b0\u589e\u81f3\u5c11\u4e00\u500b PDF \u6a94\u6848\u3002"
        return None

    # -- Slot handlers --

    def _on_files_dropped(self, paths: list[str]) -> None:
        for p in paths:
            self.file_list.add_file(Path(p))

    def _on_start_clicked(self) -> None:
        error = self.validate_before_start()
        if error:
            QMessageBox.warning(self, "\u8b66\u544a", error)
            return

        self._set_running(True)
        self.log_panel.clear()
        self.progress_panel.reset()

        files = self.file_list.get_all_files()
        try:
            self._worker = self.create_worker(files)
        except Exception as exc:
            QMessageBox.warning(self, "\u932f\u8aa4", str(exc))
            self._set_running(False)
            return

        self._worker.progress_updated.connect(self.progress_panel.update_progress)
        self._worker.log_message.connect(self.log_panel.append)
        self._worker.file_completed.connect(self._on_file_completed)
        self._worker.task_finished.connect(self._on_task_finished)
        self._worker.start()

    def _on_cancel_clicked(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.cancel()

    def _on_file_completed(self, name: str, success: bool, msg: str) -> None:
        """Can be overridden for per-file UI updates."""

    def _on_task_finished(self, success: bool, summary: str, results: list) -> None:
        self._set_running(False)
        self.progress_panel.set_finished(summary)
        if success:
            QMessageBox.information(self, "\u5b8c\u6210", summary)
        else:
            QMessageBox.warning(self, "\u63d0\u793a", summary)

    def _set_running(self, running: bool) -> None:
        self.start_btn.setEnabled(not running)
        self.cancel_btn.setEnabled(running)
        self.drop_zone.setEnabled(not running)
        self.file_list.setEnabled(not running)

    @staticmethod
    def _make_button(text: str, cls: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", cls)
        btn.setMinimumHeight(44)
        btn.setFont(QFont("Microsoft JhengHei", 13, QFont.Weight.Bold))
        return btn
