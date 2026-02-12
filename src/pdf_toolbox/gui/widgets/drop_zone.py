"""
Drag-and-drop zone widget that accepts PDF files from the file explorer.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from pdf_toolbox.gui.theme import PALETTE


class DropZone(QFrame):
    """
    A styled drop zone that accepts file drops.

    Signals:
        files_dropped(list[str]): Emitted with list of dropped file paths.
    """

    files_dropped = Signal(list)

    def __init__(
        self,
        accepted_extensions: list[str] | None = None,
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)
        self._accepted_extensions = [ext.lower() for ext in (accepted_extensions or [".pdf"])]
        self.setAcceptDrops(True)
        self.setMinimumHeight(100)
        self.setMaximumHeight(120)
        self._setup_ui()
        self._set_idle_style()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label = QLabel(
            "\u5c07 PDF \u6a94\u6848\u62d6\u653e\u5230\u6b64\u8655\n"
            "\u6216\u4f7f\u7528\u4e0b\u65b9\u6309\u9215\u700f\u89bd\u6a94\u6848"
        )
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setFont(QFont("Microsoft JhengHei", 12))
        self._label.setStyleSheet(f"color: {PALETTE.overlay1};")
        layout.addWidget(self._label)

    def _set_idle_style(self) -> None:
        self.setStyleSheet(
            f"DropZone {{ "
            f"  background-color: {PALETTE.surface0}; "
            f"  border: 2px dashed {PALETTE.surface2}; "
            f"  border-radius: 10px; "
            f"}}"
        )

    def _set_hover_style(self) -> None:
        self.setStyleSheet(
            f"DropZone {{ "
            f"  background-color: {PALETTE.surface1}; "
            f"  border: 2px dashed {PALETTE.blue}; "
            f"  border-radius: 10px; "
            f"}}"
        )

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_hover_style()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: object) -> None:  # noqa: N802
        self._set_idle_style()

    def dropEvent(self, event: QDropEvent) -> None:  # noqa: N802
        self._set_idle_style()
        paths: list[str] = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            p = Path(file_path)
            if p.is_file() and p.suffix.lower() in self._accepted_extensions:
                paths.append(str(p))
            elif p.is_dir():
                for ext in self._accepted_extensions:
                    for child in p.rglob(f"*{ext}"):
                        paths.append(str(child))
        if paths:
            self.files_dropped.emit(paths)
        event.acceptProposedAction()
