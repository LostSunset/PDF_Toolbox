# PDF Toolbox

[![CI](https://github.com/LostSunset/PDF_Toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/LostSunset/PDF_Toolbox/actions/workflows/ci.yml)
[![Release](https://github.com/LostSunset/PDF_Toolbox/actions/workflows/release.yml/badge.svg)](https://github.com/LostSunset/PDF_Toolbox/actions/workflows/release.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-green.svg)](https://doc.qt.io/qtforpython-6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

一站式 PDF 處理工具箱，採用 PySide6 構建，Catppuccin Mocha 暗色主題。

## 下載

前往 [Releases](https://github.com/LostSunset/PDF_Toolbox/releases/latest) 下載最新版 Windows 執行檔（免安裝，直接執行）。

## 功能總覽

| 功能 | 說明 |
|------|------|
| 🔓 PDF 解鎖/修復 | 多引擎修復鏈（PyMuPDF → PyPDF2 → pikepdf → Ghostscript → 複製） |
| 🖼️ PDF 轉 PNG | 使用 pdftoppm 高品質轉換，支援自訂 DPI |
| 🔒 PDF 禁止複製 | 雙層加密保護（pikepdf + PyPDF2） |
| 📎 PDF 合併 | 拖放排序，合併多個 PDF 為一個檔案 |
| ✂️ PDF 拆分 | 按範圍、每 N 頁或提取特定頁面 |
| 🔄 PDF 旋轉 | 支援 90°/180°/270° 旋轉 |
| 💧 PDF 浮水印 | 文字/圖片浮水印，可調透明度、角度、位置 |
| 📦 PDF 壓縮 | Ghostscript / PyMuPDF 雙引擎壓縮 |
| ↕️ 頁面重排序 | 自訂頁面順序，支援反轉 |

## 截圖

> 側邊欄導航 + Catppuccin Mocha 暗色主題

## 安裝

### 前置需求

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) 套件管理器
- (選用) [Ghostscript](https://www.ghostscript.com/) — 用於 PDF 壓縮
- (選用) [poppler](https://poppler.freedesktop.org/) (pdftoppm) — 用於 PDF 轉 PNG

### 快速開始

```bash
# 複製專案
git clone https://github.com/LostSunset/PDF_Toolbox.git
cd PDF_Toolbox

# 安裝依賴
uv sync

# 啟動應用程式
uv run python -m pdf_toolbox
```

## 使用方式

```bash
# 方式一：模組啟動
uv run python -m pdf_toolbox

# 方式二：指令啟動
uv run pdf-toolbox
```

啟動後透過左側側邊欄選擇功能，將 PDF 檔案拖放至工作區或點擊「新增檔案」按鈕。

## 架構

```
src/pdf_toolbox/
├── core/          # 核心邏輯（純 Python，無 Qt 依賴）
├── workers/       # QThread 背景執行緒
└── gui/           # PySide6 UI 層
    ├── widgets/   # 共用元件
    └── pages/     # 功能頁面
```

三層分離架構：**Core**（可獨立測試的純邏輯）→ **Workers**（QThread 橋接）→ **GUI**（PySide6 介面）。

## CI/CD

- **CI**：每次 push / PR 自動執行 ruff lint + pytest
- **Release**：推送 `v*` tag 時自動構建 Windows EXE 並上傳至 GitHub Releases

## 依賴套件

| 套件 | 用途 |
|------|------|
| PySide6 | GUI 框架 |
| pikepdf | PDF 合併/拆分/旋轉/重排序 |
| PyPDF2 | PDF 加密/保護 |
| PyMuPDF | PDF 解鎖/修復/浮水印/壓縮 |
| reportlab | PDF 生成輔助 |
| pycryptodome | AES 加密（PyPDF2 加密所需） |

## 開發

```bash
# 安裝開發依賴
uv sync

# 格式化 + Lint
uv run ruff format src/ tests/
uv run ruff check --fix src/ tests/

# 執行測試
uv run pytest

# 本地構建 EXE
uv run pyinstaller --name PDF_Toolbox --windowed --onefile src/pdf_toolbox/app.py
```

## 授權

[MIT License](LICENSE)
