"""
PDF 禁止複製保護工具 - PySide6 GUI 版本
支援批次處理多個 PDF 檔案
"""

import os
import sys

import pikepdf
from PyPDF2 import PdfReader, PdfWriter
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ProtectWorker(QThread):
    """處理 PDF 保護的工作執行緒"""

    progress = Signal(int, str)  # 進度百分比, 訊息
    finished_file = Signal(str, bool, str)  # 檔名, 成功與否, 訊息
    all_done = Signal()

    def __init__(self, files: list, output_dir: str):
        super().__init__()
        self.files = files
        self.output_dir = output_dir

    def run(self):
        total = len(self.files)
        for i, input_pdf in enumerate(self.files):
            filename = os.path.basename(input_pdf)
            self.progress.emit(int((i / total) * 100), f"處理中: {filename}")

            try:
                # 產生輸出檔名 p=protected
                name, ext = os.path.splitext(filename)
                output_pdf = os.path.join(self.output_dir, f"{name}_p{ext}")

                self.secure_pdf(input_pdf, output_pdf)
                self.finished_file.emit(filename, True, f"✓ {filename} → 完成")
            except Exception as e:
                self.finished_file.emit(filename, False, f"✗ {filename} → 錯誤: {e!s}")

        self.progress.emit(100, "全部完成！")
        self.all_done.emit()

    def secure_pdf(self, input_pdf: str, output_pdf: str):
        """PDF 保護核心邏輯，"""
        temp_pdf = "temp_p.pdf"

        try:
            # 使用 pikepdf 開啟並加密 PDF 檔案
            with pikepdf.open(input_pdf) as pdf:
                permissions = pikepdf.Permissions(extract=False)
                pdf.save(
                    temp_pdf, encryption=pikepdf.Encryption(user="", owner="", allow=permissions)
                )

            # 使用 PyPDF2 再次讀取並儲存為最終的加密文件
            reader = PdfReader(temp_pdf)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            # 設定權限：允許列印，但不允許複製
            writer.encrypt("", "", permissions_flag=2052)

            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)

        finally:
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)


class MainWindow(QMainWindow):
    """主視窗"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 禁止複製保護工具")
        self.setMinimumSize(700, 500)
        self.files = []
        self.output_dir = ""
        self.worker = None

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """設定 UI 元件"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 標題
        title = QLabel("📄 PDF 禁止複製保護工具")
        title.setFont(QFont("Microsoft JhengHei", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 檔案選擇區
        file_group = QGroupBox("選擇 PDF 檔案")
        file_layout = QVBoxLayout(file_group)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ 新增檔案")
        self.btn_add.clicked.connect(self.add_files)
        self.btn_clear = QPushButton("🗑️ 清除列表")
        self.btn_clear.clicked.connect(self.clear_files)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_clear)
        file_layout.addLayout(btn_layout)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(150)
        file_layout.addWidget(self.file_list)

        self.file_count_label = QLabel("已選擇 0 個檔案")
        file_layout.addWidget(self.file_count_label)

        layout.addWidget(file_group)

        # 輸出目錄區
        output_group = QGroupBox("輸出設定")
        output_layout = QHBoxLayout(output_group)

        self.output_label = QLabel("請選擇輸出資料夾...")
        self.output_label.setStyleSheet("color: #888;")
        output_layout.addWidget(self.output_label, 1)

        self.btn_output = QPushButton("📁 選擇資料夾")
        self.btn_output.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.btn_output)

        layout.addWidget(output_group)

        # 進度區
        progress_group = QGroupBox("處理進度")
        progress_layout = QVBoxLayout(progress_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("準備就緒")
        self.status_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.status_label)

        self.result_list = QListWidget()
        self.result_list.setMaximumHeight(100)
        progress_layout.addWidget(self.result_list)

        layout.addWidget(progress_group)

        # 執行按鈕
        self.btn_start = QPushButton("🚀 開始處理")
        self.btn_start.setMinimumHeight(50)
        self.btn_start.setFont(QFont("Microsoft JhengHei", 14, QFont.Bold))
        self.btn_start.clicked.connect(self.start_processing)
        layout.addWidget(self.btn_start)

    def apply_styles(self):
        """套用樣式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QWidget {
                color: #cdd6f4;
                font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
                font-size: 13px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #45475a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #89b4fa;
            }
            QPushButton {
                background-color: #45475a;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                color: #cdd6f4;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QPushButton:pressed {
                background-color: #313244;
            }
            QPushButton#startBtn {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QPushButton#startBtn:hover {
                background-color: #b4befe;
            }
            QListWidget {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #45475a;
            }
            QProgressBar {
                background-color: #313244;
                border: none;
                border-radius: 6px;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #a6e3a1;
                border-radius: 6px;
            }
            QLabel {
                color: #cdd6f4;
            }
        """)
        self.btn_start.setObjectName("startBtn")

    def add_files(self):
        """新增 PDF 檔案"""
        files, _ = QFileDialog.getOpenFileNames(self, "選擇 PDF 檔案", "", "PDF Files (*.pdf)")
        if files:
            for f in files:
                if f not in self.files:
                    self.files.append(f)
                    self.file_list.addItem(os.path.basename(f))
            self.file_count_label.setText(f"已選擇 {len(self.files)} 個檔案")

    def clear_files(self):
        """清除檔案列表"""
        self.files.clear()
        self.file_list.clear()
        self.file_count_label.setText("已選擇 0 個檔案")

    def select_output_dir(self):
        """選擇輸出資料夾"""
        directory = QFileDialog.getExistingDirectory(self, "選擇輸出資料夾")
        if directory:
            self.output_dir = directory
            self.output_label.setText(directory)
            self.output_label.setStyleSheet("color: #a6e3a1;")

    def start_processing(self):
        """開始處理"""
        if not self.files:
            QMessageBox.warning(self, "警告", "請先選擇要處理的 PDF 檔案！")
            return

        if not self.output_dir:
            QMessageBox.warning(self, "警告", "請先選擇輸出資料夾！")
            return

        # 停用按鈕
        self.btn_start.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.btn_output.setEnabled(False)

        # 清除結果列表
        self.result_list.clear()

        # 開始處理
        self.worker = ProtectWorker(self.files.copy(), self.output_dir)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished_file.connect(self.on_file_finished)
        self.worker.all_done.connect(self.on_all_done)
        self.worker.start()

    def on_progress(self, percent: int, message: str):
        """更新進度"""
        self.progress_bar.setValue(percent)
        self.status_label.setText(message)

    def on_file_finished(self, filename: str, success: bool, message: str):
        """單一檔案處理完成"""
        item = QListWidgetItem(message)
        if success:
            item.setForeground(Qt.green)
        else:
            item.setForeground(Qt.red)
        self.result_list.addItem(item)
        self.result_list.scrollToBottom()

    def on_all_done(self):
        """全部處理完成"""
        self.btn_start.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.btn_clear.setEnabled(True)
        self.btn_output.setEnabled(True)

        QMessageBox.information(
            self, "完成", f"已完成 {len(self.files)} 個檔案的處理！\n輸出位置：{self.output_dir}"
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
