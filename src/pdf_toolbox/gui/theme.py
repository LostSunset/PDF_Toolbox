"""
Catppuccin Mocha complete color palette and global stylesheet.
Reference: https://github.com/catppuccin/catppuccin
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CatppuccinMocha:
    """Complete Catppuccin Mocha palette."""

    # Accent colors
    rosewater: str = "#f5e0dc"
    flamingo: str = "#f2cdcd"
    pink: str = "#f5c2e7"
    mauve: str = "#cba6f7"
    red: str = "#f38ba8"
    maroon: str = "#eba0ac"
    peach: str = "#fab387"
    yellow: str = "#f9e2af"
    green: str = "#a6e3a1"
    teal: str = "#94e2d5"
    sky: str = "#89dceb"
    sapphire: str = "#74c7ec"
    blue: str = "#89b4fa"
    lavender: str = "#b4befe"

    # Neutral colors
    text: str = "#cdd6f4"
    subtext1: str = "#bac2de"
    subtext0: str = "#a6adc8"
    overlay2: str = "#9399b2"
    overlay1: str = "#7f849c"
    overlay0: str = "#6c7086"
    surface2: str = "#585b70"
    surface1: str = "#45475a"
    surface0: str = "#313244"
    base: str = "#1e1e2e"
    mantle: str = "#181825"
    crust: str = "#11111b"


PALETTE = CatppuccinMocha()

FONT_FAMILY = '"Microsoft JhengHei", "Segoe UI", "Noto Sans CJK TC", sans-serif'
MONO_FONT = '"Cascadia Code", "Consolas", "Courier New", monospace'


def get_stylesheet() -> str:
    """Return the global application stylesheet."""
    p = PALETTE
    return f"""
        * {{
            font-family: {FONT_FAMILY};
        }}
        QMainWindow {{
            background-color: {p.base};
        }}
        QWidget {{
            color: {p.text};
            font-size: 13px;
        }}
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {p.surface1};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px;
            color: {p.blue};
        }}
        QPushButton {{
            background-color: {p.surface1};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            color: {p.text};
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {p.surface2};
        }}
        QPushButton:pressed {{
            background-color: {p.surface0};
        }}
        QPushButton:disabled {{
            background-color: {p.surface0};
            color: {p.overlay0};
        }}
        QPushButton[class="primary"] {{
            background-color: {p.blue};
            color: {p.base};
        }}
        QPushButton[class="primary"]:hover {{
            background-color: {p.lavender};
        }}
        QPushButton[class="primary"]:pressed {{
            background-color: {p.sapphire};
        }}
        QPushButton[class="danger"] {{
            background-color: {p.red};
            color: {p.base};
        }}
        QPushButton[class="danger"]:hover {{
            background-color: {p.maroon};
        }}
        QPushButton[class="success"] {{
            background-color: {p.green};
            color: {p.base};
        }}
        QPushButton[class="success"]:hover {{
            background-color: {p.teal};
        }}
        QListWidget {{
            background-color: {p.surface0};
            border: 1px solid {p.surface1};
            border-radius: 6px;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 5px;
            border-radius: 4px;
        }}
        QListWidget::item:selected {{
            background-color: {p.surface1};
        }}
        QProgressBar {{
            background-color: {p.surface0};
            border: none;
            border-radius: 6px;
            height: 20px;
            text-align: center;
            color: {p.text};
        }}
        QProgressBar::chunk {{
            background-color: {p.green};
            border-radius: 6px;
        }}
        QTextEdit {{
            background-color: {p.surface0};
            border: 1px solid {p.surface1};
            border-radius: 6px;
            padding: 8px;
            color: {p.text};
            font-family: {MONO_FONT};
            font-size: 12px;
        }}
        QLabel {{
            color: {p.text};
        }}
        QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {{
            background-color: {p.surface0};
            border: 1px solid {p.surface1};
            border-radius: 6px;
            padding: 6px 10px;
            color: {p.text};
        }}
        QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QLineEdit:focus {{
            border-color: {p.blue};
        }}
        QComboBox::drop-down {{
            border: none;
            padding-right: 8px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {p.surface0};
            border: 1px solid {p.surface1};
            selection-background-color: {p.surface1};
            color: {p.text};
        }}
        QCheckBox {{
            color: {p.text};
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid {p.surface2};
            background-color: {p.surface0};
        }}
        QCheckBox::indicator:checked {{
            background-color: {p.blue};
            border-color: {p.blue};
        }}
        QRadioButton {{
            color: {p.text};
            spacing: 8px;
        }}
        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid {p.surface2};
            background-color: {p.surface0};
        }}
        QRadioButton::indicator:checked {{
            background-color: {p.blue};
            border-color: {p.blue};
        }}
        QScrollBar:vertical {{
            background-color: {p.mantle};
            width: 10px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {p.surface1};
            border-radius: 5px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {p.surface2};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar:horizontal {{
            background-color: {p.mantle};
            height: 10px;
            border-radius: 5px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {p.surface1};
            border-radius: 5px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {p.surface2};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        QToolTip {{
            background-color: {p.surface0};
            color: {p.text};
            border: 1px solid {p.surface1};
            border-radius: 4px;
            padding: 4px;
        }}
        QMessageBox {{
            background-color: {p.base};
        }}
        QDialog {{
            background-color: {p.base};
        }}
    """


def get_sidebar_stylesheet() -> str:
    """Return the sidebar-specific stylesheet."""
    p = PALETTE
    return f"""
        QFrame#sidebar {{
            background-color: {p.mantle};
            border-right: 1px solid {p.surface0};
        }}
        QPushButton.sidebar-btn {{
            text-align: left;
            padding: 12px 16px;
            border: none;
            border-radius: 0;
            border-left: 3px solid transparent;
            background-color: transparent;
            color: {p.subtext1};
            font-size: 13px;
            font-weight: normal;
        }}
        QPushButton.sidebar-btn:hover {{
            background-color: {p.surface0};
            color: {p.text};
        }}
        QPushButton.sidebar-btn[active="true"] {{
            background-color: {p.surface0};
            color: {p.blue};
            border-left: 3px solid {p.blue};
            font-weight: bold;
        }}
    """
