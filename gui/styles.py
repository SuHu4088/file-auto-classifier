DARK_STYLE = """
QMainWindow {
    background-color: #1a1a2e;
    color: #ffffff;
}

QWidget {
    background-color: #1a1a2e;
    color: #ffffff;
}

QFrame {
    background-color: #16213e;
    border-radius: 8px;
    border: 1px solid #0f3460;
}

QLineEdit {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #e94560;
    outline: none;
}

QPushButton {
    background-color: #0f3460;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #ffffff;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #e94560;
}

QPushButton:pressed {
    background-color: #c73e54;
}

QPushButton:disabled {
    background-color: #2d3436;
    color: #636e72;
}

QProgressBar {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    height: 20px;
    text-align: center;
    color: #ffffff;
    font-size: 12px;
}

QProgressBar::chunk {
    background-color: #e94560;
    border-radius: 5px;
}

QTextEdit {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 10px;
    color: #ffffff;
    font-family: "Consolas", "Monaco", monospace;
    font-size: 12px;
}

QTreeWidget {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    color: #ffffff;
    font-size: 13px;
}

QTreeWidget::item {
    padding: 6px 10px;
}

QTreeWidget::item:selected {
    background-color: #0f3460;
}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {
    border-image: none;
}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {
    border-image: none;
}

QGroupBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 8px;
    padding: 15px;
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QLabel {
    color: #ffffff;
    font-size: 13px;
}

QComboBox {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
}

QComboBox::drop-down {
    border-left: 1px solid #0f3460;
    border-radius: 0 6px 6px 0;
}

QComboBox QAbstractItemView {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 6px;
    color: #ffffff;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #0f3460;
}

QDockWidget {
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}

QDockWidget::title {
    background-color: #16213e;
    padding: 8px 10px;
    border-bottom: 1px solid #0f3460;
}

QScrollBar:vertical {
    background-color: #16213e;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #0f3460;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #e94560;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #16213e;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #0f3460;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #e94560;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QStatusBar {
    background-color: #16213e;
    border-top: 1px solid #0f3460;
    color: #a0a0a0;
    font-size: 12px;
}

QToolTip {
    background-color: #0f3460;
    border: 1px solid #e94560;
    border-radius: 4px;
    padding: 6px 10px;
    color: #ffffff;
    font-size: 12px;
}
"""