"""
Password input dialog for encrypted PDFs.
"""

from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PasswordDialog(QDialog):
    """Modal dialog for entering a PDF password."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("\u8f38\u5165 PDF \u5bc6\u78bc")
        self.setFixedSize(380, 180)
        self._password: str | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        label = QLabel("\u8acb\u8f38\u5165 PDF \u5bc6\u78bc\uff1a")
        label.setFont(QFont("Microsoft JhengHei", 12))
        layout.addWidget(label)

        self._input = QLineEdit()
        self._input.setEchoMode(QLineEdit.EchoMode.Password)
        self._input.returnPressed.connect(self.accept)
        layout.addWidget(self._input)

        self._show_pw = QCheckBox("\u986f\u793a\u5bc6\u78bc")
        self._show_pw.toggled.connect(
            lambda on: self._input.setEchoMode(
                QLineEdit.EchoMode.Normal if on else QLineEdit.EchoMode.Password
            )
        )
        layout.addWidget(self._show_pw)

        btn_row = QHBoxLayout()
        ok_btn = QPushButton("\u78ba\u5b9a")
        ok_btn.setProperty("class", "primary")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("\u53d6\u6d88")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def accept(self) -> None:
        self._password = self._input.text()
        super().accept()

    @property
    def password(self) -> str | None:
        """Return the entered password, or None if cancelled."""
        return self._password

    @staticmethod
    def get_password(parent: QWidget | None = None) -> str | None:
        """Convenience method. Returns password or None if cancelled."""
        dialog = PasswordDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.password
        return None
