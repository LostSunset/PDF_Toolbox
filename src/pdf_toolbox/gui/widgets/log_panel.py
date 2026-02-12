"""
Scrollable log output panel.
"""

from __future__ import annotations

from PySide6.QtWidgets import QGroupBox, QTextEdit, QVBoxLayout, QWidget


class LogPanel(QWidget):
    """Read-only log display in a group box."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("\u57f7\u884c\u65e5\u8a8c")
        group_layout = QVBoxLayout(group)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setMinimumHeight(120)
        group_layout.addWidget(self._text)

        layout.addWidget(group)

    def append(self, message: str) -> None:
        """Append a log message and scroll to bottom."""
        self._text.append(message)
        sb = self._text.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear(self) -> None:
        """Clear all log messages."""
        self._text.clear()
