# 文件自动分类器 (File Auto Classifier)

> **本仓库已并入 folder-ops，后续维护请前往 https://github.com/SuHu4088/folder-ops**


![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-green?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

一款基于 PySide6 开发的桌面文件自动分类工具，能够根据文件类型自动将杂乱无章的文件归类到对应的子文件夹中，让文件管理变得轻松高效。

![主界面截图](screenshots/main_interface.png)

## 目录

- [项目概述](#项目概述)
- [功能特性](#功能特性)
- [安装指南](#安装指南)
- [使用方法](#使用方法)
- [项目结构](#项目结构)
- [贡献说明](#贡献说明)
- [许可证](#许可证)

## 项目概述

在日常使用电脑的过程中，下载文件夹、桌面等位置经常会堆积大量杂乱的文件——视频、图片、文档、安装包混杂在一起，手动整理费时费力。

**文件自动分类器** 旨在解决这个问题。只需选择一个文件夹，程序会自动扫描其中的所有文件，根据扩展名智能分类，将视频、图片、文本、音频等不同类型的文件分别移动到对应的子文件夹中，一键完成文件整理工作。

### 核心价值

- **高效**：一键自动分类数百个文件，替代繁琐的手动整理
- **安全**：采用原子操作 + 完整性验证的文件移动机制，确保数据安全
- **直观**：深色主题 GUI 界面，实时进度显示，操作日志全程记录
- **可扩展**：分类规则配置化，轻松添加新的文件类别

## 功能特性

### 智能分类

支持 10 种文件类别，覆盖日常使用的主流文件格式：

| 类别 | 支持的扩展名 |
|------|-------------|
| 视频 | mp4, mkv, avi, mov, wmv, flv, webm, m4v, mpeg, mpg, 3gp, rm, rmvb |
| 图片 | jpg, jpeg, png, gif, bmp, tiff, webp, svg, ico, heic, raw |
| 文本 | txt, md, doc, docx, pdf, xlsx, pptx, csv, rtf, epub, mobi |
| 音频 | mp3, wav, flac, aac, ogg, wma, m4a, alac, ape, opus |
| 压缩 | zip, rar, 7z, tar, gz, bz2, xz, iso, cab |
| 安装包 | exe, msi, apk, dmg, pkg |
| 代码 | py, js, ts, html, css, java, cpp, go, rs, json, yaml |
| 程序 | dll, so, bat, cmd, sh, ps1 |
| 数据库 | db, sqlite, mdb, accdb, bak |
| 其他 | 未匹配的文件自动归入此类 |

### 核心功能

- **文件夹选择**：支持浏览对话框选择或直接拖拽文件夹到窗口
- **预览模式**：分类前预览文件列表，查看各类文件数量和大小
- **实时进度**：进度条 + 百分比显示，操作日志全程记录
- **重复文件处理**：支持重命名、跳过、覆盖三种策略
- **随时停止**：分类过程中可随时停止操作
- **窗口居中**：启动时自动居中屏幕显示

### 技术特性

- **深色主题**：护眼的深色界面，适合长时间使用
- **多线程处理**：使用 QThread 执行文件操作，界面不卡顿
- **安全文件移动**：同文件系统使用原子操作 `os.rename()`，跨文件系统使用 `copy2()` + 完整性验证 + `remove()`
- **信号槽通信**：线程间通过 Qt 信号槽机制通信，线程安全

## 安装指南

### 环境要求

- **Python** 3.8 或更高版本
- **PySide6** 6.5 或更高版本
- 操作系统：Windows / Linux / macOS

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/file-auto-classifier.git
cd file-auto-classifier
```

2. **创建虚拟环境（推荐）**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

## 使用方法

### 启动程序

```bash
python main.py
```

### 操作流程

1. **选择文件夹**
   - 点击「浏览」按钮，在弹出的对话框中选择目标文件夹
   - 或直接将文件夹拖拽到程序窗口中

2. **预览分类结果（可选）**
   - 点击「预览」按钮，程序会扫描文件夹并显示分类预览
   - 左侧树形视图展示各类别的文件数量和总大小
   - 可展开查看每个类别下的具体文件列表

3. **设置重复文件策略**
   - **重命名**：目标已存在同名文件时，自动添加序号（如 `file_1.txt`）
   - **跳过**：跳过已存在的文件，不做任何操作
   - **覆盖**：删除目标已存在的文件，用新文件替换

4. **开始分类**
   - 点击「开始分类」按钮，程序弹出确认对话框
   - 确认后开始执行文件分类，进度条实时更新
   - 右侧日志区域显示每个文件的处理结果
   - 分类过程中可点击「停止」按钮中断操作

5. **查看结果**
   - 分类完成后，日志区域显示统计信息（成功/失败/跳过数量）
   - 目标文件夹中会自动创建分类子文件夹

## 项目结构

```
file-auto-classifier/
├── main.py                      # 程序入口
├── requirements.txt            # 依赖列表
├── LICENSE                      # MIT 许可证
├── README.md                    # 项目说明文档
├── .gitignore                   # Git 忽略规则
│
├── core/                        # 核心业务逻辑模块
│   ├── __init__.py
│   ├── category_config.py       # 文件类型分类配置
│   ├── file_utils.py            # 文件操作工具函数
│   └── classifier.py           # 文件分类器（QThread）
│
├── gui/                         # 图形界面模块
│   ├── __init__.py
│   ├── main_window.py           # 主窗口界面与事件处理
│   └── styles.py               # 深色主题样式表
│
├── docs/                        # 文档目录
│   └── 开发文档.md              # 详细开发文档
│
└── screenshots/                 # 截图目录
    └── main_interface.png       # 程序主界面截图
```

## 贡献说明

欢迎为本项目贡献代码！请遵循以下流程：

### 提交 Issue

- 使用前请先搜索是否已有相关 Issue
- 提交 Issue 时请描述清楚问题或建议，附上截图和复现步骤

### 提交 PR

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 代码规范

- 遵循 [PEP 8](https://pep8.org/) 编码规范
- 模块名使用小写蛇形命名（如 `file_utils.py`）
- 类名使用大驼峰命名（如 `FileClassifier`）
- 函数和变量名使用小写蛇形命名（如 `get_category()`）
- 常量名使用大写蛇形命名（如 `EXTENSION_CATEGORIES`）

### 扩展指南

如需添加新的文件分类类别，只需在 [core/category_config.py](core/category_config.py) 中修改 `EXTENSION_CATEGORIES` 和 `CATEGORY_COLORS` 字典即可，无需修改其他代码。

## 许可证

本项目基于 [MIT License](LICENSE) 开源，可自由使用、修改和分发。
