"""
Unified file list widget with drag-reorder, delete, and add support.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FileListWidget(QWidget):
    """
    Reusable file list component.

    Features:
        - Add files / folders via buttons
        - Delete selected via button or Delete key
        - Drag-and-drop reorder (internal, optional)
        - File count label
    """

    def __init__(self, allow_reorder: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._files: list[Path] = []
        self._allow_reorder = allow_reorder
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Buttons row
        btn_row = QHBoxLayout()
        self.btn_add_files = QPushButton("\u2795 \u65b0\u589e\u6a94\u6848")
        self.btn_add_files.clicked.connect(self._browse_files)
        self.btn_add_folder = QPushButton("\U0001f4c1 \u65b0\u589e\u8cc7\u6599\u593e")
        self.btn_add_folder.clicked.connect(self._browse_folder)
        self.btn_remove = QPushButton("\u2796 \u79fb\u9664\u9078\u53d6")
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_clear = QPushButton("\U0001f5d1\ufe0f \u6e05\u9664\u5168\u90e8")
        self.btn_clear.clicked.connect(self.clear)
        btn_row.addWidget(self.btn_add_files)
        btn_row.addWidget(self.btn_add_folder)
        btn_row.addWidget(self.btn_remove)
        btn_row.addWidget(self.btn_clear)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # List
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_widget.setMinimumHeight(120)
        if self._allow_reorder:
            self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        layout.addWidget(self.list_widget)

        # Count label
        self._count_label = QLabel("\u5df2\u9078\u64c7 0 \u500b\u6a94\u6848")
        layout.addWidget(self._count_label)

        # Delete key binding
        self.list_widget.installEventFilter(self)

    # -- Public API --

    def add_file(self, path: Path) -> None:
        """Add a single file to the list (no duplicates)."""
        if path not in self._files:
            self._files.append(path)
            self.list_widget.addItem(str(path))
            self._update_count()

    def add_files(self, paths: list[Path]) -> None:
        """Add multiple files."""
        for p in paths:
            self.add_file(p)

    def remove_selected(self) -> None:
        """Remove all selected items from the list."""
        for item in reversed(self.list_widget.selectedItems()):
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)
            del self._files[row]
        self._update_count()

    def clear(self) -> None:
        """Clear the entire list."""
        self._files.clear()
        self.list_widget.clear()
        self._update_count()

    def count(self) -> int:
        """Return the number of files in the list."""
        return len(self._files)

    def get_all_files(self) -> list[Path]:
        """Return files in current display order (respects reorder)."""
        if self._allow_reorder:
            return [Path(self.list_widget.item(i).text()) for i in range(self.list_widget.count())]
        return list(self._files)

    # -- Internal --

    def _browse_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "\u9078\u64c7 PDF \u6a94\u6848",
            "",
            "PDF Files (*.pdf);;All Files (*.*)",
        )
        for f in files:
            self.add_file(Path(f))

    def _browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "\u9078\u64c7\u8cc7\u6599\u593e")
        if folder:
            for pdf in Path(folder).rglob("*.pdf"):
                self.add_file(pdf)

    def _update_count(self) -> None:
        n = self.count()
        self._count_label.setText(f"\u5df2\u9078\u64c7 {n} \u500b\u6a94\u6848")

    def eventFilter(self, obj: object, event: QEvent) -> bool:  # noqa: N802
        if (
            obj is self.list_widget
            and event.type() == QEvent.Type.KeyPress
            and event.key() == Qt.Key.Key_Delete
        ):
            self.remove_selected()
            return True
        return super().eventFilter(obj, event)
