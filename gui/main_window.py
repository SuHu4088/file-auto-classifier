import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QGroupBox, QLabel,
    QComboBox, QFrame, QSizePolicy, QMessageBox
)
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QColor

from core.classifier import FileClassifier, FilePreviewer
from core.category_config import get_category_color
from core.file_utils import format_file_size


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.classifier = None
        self.preview_data = {}
        self.init_ui()
        self.center_window()

    def init_ui(self):
        self.setWindowTitle("文件自动分类器")
        self.setMinimumSize(900, 650)
        self.setMaximumSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        top_section = self.create_top_section()
        main_layout.addWidget(top_section)

        middle_section = self.create_middle_section()
        main_layout.addWidget(middle_section)

        bottom_section = self.create_bottom_section()
        main_layout.addWidget(bottom_section)

        self.statusBar().showMessage("就绪")

    def create_top_section(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("📁 文件自动分类器")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e94560;")
        layout.addWidget(title_label)

        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("请输入文件夹路径，或拖拽文件夹到此处...")
        self.path_edit.setReadOnly(True)
        self.path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        path_layout.addWidget(self.path_edit)

        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_folder)
        path_layout.addWidget(browse_btn)

        layout.addLayout(path_layout)

        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)

        conflict_label = QLabel("重复文件处理:")
        options_layout.addWidget(conflict_label)

        self.conflict_combo = QComboBox()
        self.conflict_combo.addItems(["重命名", "跳过", "覆盖"])
        options_layout.addWidget(self.conflict_combo)

        options_layout.addStretch()

        stats_label = QLabel()
        self.stats_label = stats_label
        stats_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        options_layout.addWidget(stats_label)

        layout.addLayout(options_layout)

        return frame

    def create_middle_section(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        left_group = QGroupBox("分类预览")
        left_layout = QVBoxLayout(left_group)

        self.preview_tree = QTreeWidget()
        self.preview_tree.setHeaderLabels(["类别", "数量", "大小"])
        self.preview_tree.setColumnWidth(0, 120)
        self.preview_tree.setColumnWidth(1, 60)
        self.preview_tree.setColumnWidth(2, 100)
        left_layout.addWidget(self.preview_tree)

        right_group = QGroupBox("操作日志")
        right_layout = QVBoxLayout(right_group)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        right_layout.addWidget(self.log_text)

        layout.addWidget(left_group, 1)
        layout.addWidget(right_group, 1)

        return frame

    def create_bottom_section(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        progress_label_layout = QHBoxLayout()
        progress_label_layout.setSpacing(15)

        self.progress_label = QLabel("等待操作...")
        self.progress_label.setStyleSheet("color: #e94560; font-weight: 500;")
        progress_label_layout.addWidget(self.progress_label)

        progress_label_layout.addStretch()

        self.file_count_label = QLabel("")
        self.file_count_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        progress_label_layout.addWidget(self.file_count_label)

        layout.addLayout(progress_label_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.preview_btn = QPushButton("预览")
        self.preview_btn.clicked.connect(self.preview_files)
        button_layout.addWidget(self.preview_btn)

        self.start_btn = QPushButton("开始分类")
        self.start_btn.clicked.connect(self.start_classification)
        button_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_classification)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        exit_btn = QPushButton("退出")
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)

        layout.addLayout(button_layout)

        return frame

    def center_window(self):
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def browse_folder(self):
        from PySide6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(
            self, "选择要分类的文件夹",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.path_edit.setText(folder)
            self.log_text.append(f"📂 已选择文件夹: {folder}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.path_edit.setText(folder_path)
                self.log_text.append(f"📂 已选择文件夹: {folder_path}")

    def preview_files(self):
        folder_path = self.path_edit.text().strip()
        if not folder_path or not os.path.isdir(folder_path):
            QMessageBox.warning(self, "警告", "请先选择有效的文件夹路径")
            return

        self.log_text.append("🔍 正在预览文件...")
        self.statusBar().showMessage("正在预览文件...")

        self.preview_data = FilePreviewer.preview(folder_path)

        self.preview_tree.clear()

        if self.preview_data["total"] == 0:
            self.log_text.append("⚠️ 文件夹中没有文件")
            self.statusBar().showMessage("文件夹中没有文件")
            return

        self.stats_label.setText(f"文件总数: {self.preview_data['total']}")

        for category, data in self.preview_data["categories"].items():
            color = QColor(get_category_color(category))
            item = QTreeWidgetItem([category, str(data["count"]), data["formatted_size"]])
            item.setForeground(0, color)
            item.setForeground(1, color)
            item.setForeground(2, color)

            for file_name in data["files"][:20]:
                sub_item = QTreeWidgetItem([file_name, "", ""])
                sub_item.setForeground(0, QColor("#a0a0a0"))
                item.addChild(sub_item)

            if len(data["files"]) > 20:
                sub_item = QTreeWidgetItem([f"... 还有 {len(data['files']) - 20} 个文件", "", ""])
                sub_item.setForeground(0, QColor("#636e72"))
                item.addChild(sub_item)

            self.preview_tree.addTopLevelItem(item)

        total_size = sum(data["size"] for data in self.preview_data["categories"].values())
        self.log_text.append(f"✅ 预览完成！共 {self.preview_data['total']} 个文件，总大小 {format_file_size(total_size)}")
        self.statusBar().showMessage(f"预览完成！共 {self.preview_data['total']} 个文件")

    def start_classification(self):
        folder_path = self.path_edit.text().strip()
        if not folder_path or not os.path.isdir(folder_path):
            QMessageBox.warning(self, "警告", "请先选择有效的文件夹路径")
            return

        confirm = QMessageBox.question(
            self, "确认分类",
            f"确定要对文件夹 '{folder_path}' 进行文件分类吗？\n\n"
            "此操作将移动文件到对应的分类文件夹中。",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        conflict_strategy = {
            "重命名": "rename",
            "跳过": "skip",
            "覆盖": "overwrite"
        }[self.conflict_combo.currentText()]

        self.classifier = FileClassifier(folder_path, conflict_strategy)
        self.classifier.progress_updated.connect(self.update_progress)
        self.classifier.status_updated.connect(self.update_status)
        self.classifier.log_added.connect(self.add_log)
        self.classifier.classification_completed.connect(self.on_classification_completed)

        self.preview_btn.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.clear_btn.setEnabled(False)
        self.conflict_combo.setEnabled(False)

        self.progress_bar.setValue(0)
        self.log_text.append("🚀 开始分类...")
        self.classifier.start()

    def stop_classification(self):
        if self.classifier and self.classifier.isRunning():
            self.classifier.stop()
            self.log_text.append("⏹️ 正在停止分类...")
            self.stop_btn.setEnabled(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"进度: {value}%")

    def update_status(self, status):
        self.statusBar().showMessage(status)

    def add_log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def on_classification_completed(self, results):
        self.preview_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.clear_btn.setEnabled(True)
        self.conflict_combo.setEnabled(True)

        if results:
            self.log_text.append(f"\n📊 分类统计:")
            for category, data in results.get("categories", {}).items():
                self.log_text.append(f"   {category}: {data['count']} 个文件")

            total_success = results.get("success", 0)
            total_failed = results.get("failed", 0)
            total_skipped = results.get("skipped", 0)

            if total_success > 0:
                self.log_text.append(f"\n🎉 成功移动 {total_success} 个文件")
            if total_failed > 0:
                self.log_text.append(f"❌ {total_failed} 个文件移动失败")
            if total_skipped > 0:
                self.log_text.append(f"○ {total_skipped} 个文件已跳过")

        self.statusBar().showMessage("分类完成")

    def clear_all(self):
        self.path_edit.clear()
        self.preview_tree.clear()
        self.log_text.clear()
        self.progress_bar.setValue(0)
        self.progress_label.setText("等待操作...")
        self.file_count_label.clear()
        self.stats_label.clear()
        self.preview_data = {}
        self.statusBar().showMessage("就绪")

    def closeEvent(self, event):
        if self.classifier and self.classifier.isRunning():
            confirm = QMessageBox.question(
                self, "确认退出",
                "分类正在进行中，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm != QMessageBox.Yes:
                event.ignore()
                return
            self.classifier.stop()
        event.accept()