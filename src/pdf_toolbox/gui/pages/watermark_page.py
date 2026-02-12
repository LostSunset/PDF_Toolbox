"""
PDF Watermark page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
)

from pdf_toolbox.core.watermark import WatermarkConfig
from pdf_toolbox.gui.pages.base_page import BasePage
from pdf_toolbox.workers.base_worker import BaseWorker
from pdf_toolbox.workers.watermark_worker import WatermarkWorker


class WatermarkPage(BasePage):
    """PDF watermark page with text and image modes."""

    def __init__(self, parent: BasePage | None = None) -> None:
        super().__init__(
            title="\U0001f4a7 PDF \u6d6e\u6c34\u5370",
            description=(
                "\u65b0\u589e\u6587\u5b57\u6216\u5716\u7247\u6d6e\u6c34\u5370\uff0c"
                "\u652f\u63f4\u900f\u660e\u5ea6\u3001\u89d2\u5ea6\u548c\u4f4d\u7f6e\u8a2d\u5b9a\u3002"
            ),
            parent=parent,
        )
        self._image_path: Path | None = None

    def build_settings_area(self, layout: QVBoxLayout) -> None:
        # Type selection
        type_row = QHBoxLayout()
        self._type_group = QButtonGroup(self)
        self._text_radio = QRadioButton("\u6587\u5b57\u6d6e\u6c34\u5370")
        self._text_radio.setChecked(True)
        self._image_radio = QRadioButton("\u5716\u7247\u6d6e\u6c34\u5370")
        self._type_group.addButton(self._text_radio)
        self._type_group.addButton(self._image_radio)
        type_row.addWidget(self._text_radio)
        type_row.addWidget(self._image_radio)
        type_row.addStretch()
        layout.addLayout(type_row)

        # Text input
        text_row = QHBoxLayout()
        text_row.addWidget(QLabel("\u6587\u5b57:"))
        self._text_input = QLineEdit()
        self._text_input.setPlaceholderText("\u4f8b: CONFIDENTIAL")
        text_row.addWidget(self._text_input)
        layout.addLayout(text_row)

        # Image input
        img_row = QHBoxLayout()
        img_row.addWidget(QLabel("\u5716\u7247:"))
        self._image_label = QLabel("\u672a\u9078\u64c7\u5716\u7247")
        img_row.addWidget(self._image_label, 1)
        self._image_btn = QPushButton("\u700f\u89bd")
        self._image_btn.clicked.connect(self._browse_image)
        img_row.addWidget(self._image_btn)
        layout.addLayout(img_row)

        # Parameters
        params_row = QHBoxLayout()
        params_row.addWidget(QLabel("\u900f\u660e\u5ea6:"))
        self._opacity_spin = QDoubleSpinBox()
        self._opacity_spin.setRange(0.01, 1.0)
        self._opacity_spin.setValue(0.3)
        self._opacity_spin.setSingleStep(0.05)
        params_row.addWidget(self._opacity_spin)

        params_row.addWidget(QLabel("\u89d2\u5ea6:"))
        self._angle_spin = QSpinBox()
        self._angle_spin.setRange(-180, 180)
        self._angle_spin.setValue(-45)
        self._angle_spin.setSuffix("\u00b0")
        params_row.addWidget(self._angle_spin)

        params_row.addWidget(QLabel("\u4f4d\u7f6e:"))
        self._position_combo = QComboBox()
        self._position_combo.addItems(
            [
                "center",
                "top-left",
                "top-right",
                "bottom-left",
                "bottom-right",
            ]
        )
        params_row.addWidget(self._position_combo)

        params_row.addWidget(QLabel("\u5b57\u578b\u5927\u5c0f:"))
        self._fontsize_spin = QSpinBox()
        self._fontsize_spin.setRange(8, 200)
        self._fontsize_spin.setValue(48)
        params_row.addWidget(self._fontsize_spin)

        params_row.addStretch()
        layout.addLayout(params_row)

    def _browse_image(self) -> None:
        f, _ = QFileDialog.getOpenFileName(
            self,
            "\u9078\u64c7\u5716\u7247",
            "",
            "Images (*.png *.jpg *.jpeg *.svg);;All (*.*)",
        )
        if f:
            self._image_path = Path(f)
            self._image_label.setText(f)

    def create_worker(self, files: list[Path]) -> BaseWorker:
        config = WatermarkConfig(
            text=self._text_input.text() if self._text_radio.isChecked() else "",
            image_path=self._image_path if self._image_radio.isChecked() else None,
            opacity=self._opacity_spin.value(),
            angle=self._angle_spin.value(),
            position=self._position_combo.currentText(),
            font_size=self._fontsize_spin.value(),
        )
        out_dir = self.output_dir_selector.get_output_dir(files[0] if files else None)
        return WatermarkWorker(files, config=config, output_dir=out_dir)
