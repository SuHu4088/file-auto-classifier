"""截图辅助脚本 - 启动程序并自动截图"""
import sys
import os
import time
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication
from gui.main_window import MainWindow
from gui.styles import DARK_STYLE


def create_test_files():
    """创建测试文件夹和测试文件"""
    test_dir = os.path.join(tempfile.gettempdir(), "file_classifier_test")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    test_files = {
        "video1.mp4": 1024 * 1024 * 50,
        "video2.mkv": 1024 * 1024 * 30,
        "photo1.jpg": 1024 * 500,
        "photo2.png": 1024 * 800,
        "photo3.gif": 1024 * 200,
        "document1.pdf": 1024 * 100,
        "document2.docx": 1024 * 150,
        "notes.txt": 1024 * 5,
        "music1.mp3": 1024 * 1024 * 8,
        "music2.flac": 1024 * 1024 * 25,
        "archive1.zip": 1024 * 1024 * 10,
        "archive2.rar": 1024 * 1024 * 5,
        "setup1.exe": 1024 * 1024 * 20,
        "script1.py": 1024 * 3,
        "script2.js": 1024 * 2,
        "data.json": 1024 * 1,
        "config.yaml": 1024 * 1,
        "unknown.xyz": 1024 * 100,
    }

    for name, size in test_files.items():
        file_path = os.path.join(test_dir, name)
        with open(file_path, 'wb') as f:
            f.seek(size - 1)
            f.write(b'\x00')

    return test_dir


def main():
    test_dir = create_test_files()

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)

    window = MainWindow()
    window.show()

    # 设置测试文件夹路径
    window.path_edit.setText(test_dir)

    # 执行预览
    QTimer.singleShot(500, lambda: window.preview_files())

    # 截图
    def take_screenshot():
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(window.winId())

        # 主界面截图
        screenshot_path = os.path.join(screenshots_dir, "main_interface.png")
        screenshot.save(screenshot_path, "png")
        print(f"截图已保存: {screenshot_path}")

        # 清理测试文件
        shutil.rmtree(test_dir)

        app.quit()

    QTimer.singleShot(2000, take_screenshot)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
