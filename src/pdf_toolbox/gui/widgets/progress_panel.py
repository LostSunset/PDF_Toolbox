"""
Unified progress bar + status label panel.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QLabel, QProgressBar, QVBoxLayout, QWidget


class ProgressPanel(QWidget):
    """Progress bar with status message in a group box."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("\u8655\u7406\u9032\u5ea6")
        group_layout = QVBoxLayout(group)

        self._bar = QProgressBar()
        self._bar.setValue(0)
        group_layout.addWidget(self._bar)

        self._label = QLabel("\u6e96\u5099\u5c31\u7dd2")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        group_layout.addWidget(self._label)

        layout.addWidget(group)

    def update_progress(self, current: int, total: int, message: str) -> None:
        """Update the progress bar and status label."""
        percentage = int((current / total) * 100) if total > 0 else 0
        self._bar.setValue(percentage)
        self._label.setText(f"{message}  ({current}/{total})")

    def reset(self) -> None:
        """Reset to initial state."""
        self._bar.setValue(0)
        self._label.setText("\u6e96\u5099\u5c31\u7dd2")

    def set_finished(self, summary: str) -> None:
        """Set the panel to finished state."""
        self._bar.setValue(100)
        self._label.setText(summary)
