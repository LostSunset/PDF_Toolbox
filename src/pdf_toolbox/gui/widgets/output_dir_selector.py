"""
Output directory selection widget.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pdf_toolbox.gui.theme import PALETTE


class OutputDirSelector(QWidget):
    """
    Lets the user pick an output folder, or choose "same as source".

    Signals:
        directory_changed(str): Emitted when directory changes.
    """

    directory_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._directory: str = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("\u8f38\u51fa\u8a2d\u5b9a")
        group_layout = QVBoxLayout(group)

        self._same_as_source = QCheckBox(
            "\u5132\u5b58\u5728\u539f\u59cb\u6a94\u6848\u540c\u4e00\u76ee\u9304"
        )
        self._same_as_source.setChecked(True)
        self._same_as_source.toggled.connect(self._on_toggle)
        group_layout.addWidget(self._same_as_source)

        row = QHBoxLayout()
        self._label = QLabel("\u4f7f\u7528\u539f\u59cb\u6a94\u6848\u76ee\u9304")
        self._label.setStyleSheet(f"color: {PALETTE.overlay1};")
        row.addWidget(self._label, 1)
        self._btn = QPushButton("\U0001f4c1 \u9078\u64c7\u8cc7\u6599\u593e")
        self._btn.clicked.connect(self._browse)
        self._btn.setEnabled(False)
        row.addWidget(self._btn)
        group_layout.addLayout(row)

        layout.addWidget(group)

    def _on_toggle(self, checked: bool) -> None:
        self._btn.setEnabled(not checked)
        if checked:
            self._label.setText("\u4f7f\u7528\u539f\u59cb\u6a94\u6848\u76ee\u9304")
            self._label.setStyleSheet(f"color: {PALETTE.overlay1};")
            self._directory = ""
        else:
            self._label.setText("\u8acb\u9078\u64c7\u8f38\u51fa\u8cc7\u6599\u593e...")
            self._label.setStyleSheet(f"color: {PALETTE.overlay1};")

    def _browse(self) -> None:
        d = QFileDialog.getExistingDirectory(self, "\u9078\u64c7\u8f38\u51fa\u8cc7\u6599\u593e")
        if d:
            self._directory = d
            self._label.setText(d)
            self._label.setStyleSheet(f"color: {PALETTE.green};")
            self.directory_changed.emit(d)

    def get_output_dir(self, source_path: Path | None = None) -> Path:
        """Return the effective output directory."""
        if self._same_as_source.isChecked() and source_path:
            return source_path.parent
        if self._directory:
            return Path(self._directory)
        if source_path:
            return source_path.parent
        return Path(".")

    @property
    def use_same_as_source(self) -> bool:
        """Whether 'same as source' is checked."""
        return self._same_as_source.isChecked()
