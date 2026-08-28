import os
from PySide6.QtCore import QThread, Signal
from core.category_config import get_category
from core.file_utils import get_files_in_folder, ensure_folder_exists, move_file, format_file_size

class FileClassifier(QThread):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    log_added = Signal(str)
    classification_completed = Signal(dict)

    def __init__(self, folder_path, conflict_strategy="rename"):
        super().__init__()
        self.folder_path = folder_path
        self.conflict_strategy = conflict_strategy
        self.is_running = True

    def run(self):
        self.status_updated.emit("正在扫描文件...")
        files = get_files_in_folder(self.folder_path)
        
        if not files:
            self.log_added.emit("未找到任何文件")
            self.classification_completed.emit({})
            return

        self.status_updated.emit(f"找到 {len(files)} 个文件")
        self.log_added.emit(f"开始分类，共 {len(files)} 个文件")

        category_files = {}
        for file_info in files:
            category = get_category(file_info["extension"])
            if category not in category_files:
                category_files[category] = []
            category_files[category].append(file_info)

        total_files = len(files)
        processed_count = 0
        results = {
            "total": total_files,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "categories": {}
        }

        for category, file_list in category_files.items():
            dest_folder = os.path.join(self.folder_path, category)
            ensure_folder_exists(dest_folder)
            
            results["categories"][category] = {
                "count": len(file_list),
                "size": sum(f["size"] for f in file_list),
                "files": []
            }

            for file_info in file_list:
                if not self.is_running:
                    self.status_updated.emit("分类已停止")
                    self.classification_completed.emit(results)
                    return

                dest_path = os.path.join(dest_folder, file_info["name"])
                success, message = move_file(
                    file_info["path"],
                    dest_folder,
                    self.conflict_strategy
                )

                processed_count += 1
                progress = int((processed_count / total_files) * 100)
                self.progress_updated.emit(progress)

                if success:
                    results["success"] += 1
                    results["categories"][category]["files"].append(file_info["name"])
                    self.log_added.emit(f"✓ [{category}] {file_info['name']}")
                elif "已跳过" in message:
                    results["skipped"] += 1
                    self.log_added.emit(f"○ [{category}] {file_info['name']} - {message}")
                else:
                    results["failed"] += 1
                    self.log_added.emit(f"✗ [{category}] {file_info['name']} - {message}")

        self.status_updated.emit("分类完成")
        self.progress_updated.emit(100)
        
        summary = f"分类完成！成功: {results['success']}, 失败: {results['failed']}, 跳过: {results['skipped']}"
        self.log_added.emit(summary)
        self.classification_completed.emit(results)

    def stop(self):
        self.is_running = False

class FilePreviewer:
    @staticmethod
    def preview(folder_path):
        files = get_files_in_folder(folder_path)
        category_files = {}
        
        for file_info in files:
            category = get_category(file_info["extension"])
            if category not in category_files:
                category_files[category] = []
            category_files[category].append(file_info)

        preview_data = {
            "total": len(files),
            "categories": {}
        }

        for category, file_list in category_files.items():
            total_size = sum(f["size"] for f in file_list)
            preview_data["categories"][category] = {
                "count": len(file_list),
                "size": total_size,
                "formatted_size": format_file_size(total_size),
                "files": [f["name"] for f in file_list]
            }

        return preview_data