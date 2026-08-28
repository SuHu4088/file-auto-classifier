import os
import shutil

def get_files_in_folder(folder_path):
    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            try:
                file_size = os.path.getsize(item_path)
                files.append({
                    "name": item,
                    "path": item_path,
                    "size": file_size,
                    "extension": os.path.splitext(item)[1][1:].lower()
                })
            except (OSError, IOError):
                continue
    return files

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

def generate_new_filename(dest_path):
    if not os.path.exists(dest_path):
        return dest_path
    
    dir_name = os.path.dirname(dest_path)
    file_name = os.path.basename(dest_path)
    name, ext = os.path.splitext(file_name)
    
    counter = 1
    while True:
        new_name = f"{name}_{counter}{ext}"
        new_path = os.path.join(dir_name, new_name)
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def move_file(src_path, dest_folder, conflict_strategy="rename"):
    dest_path = os.path.join(dest_folder, os.path.basename(src_path))
    
    if os.path.exists(dest_path):
        if conflict_strategy == "skip":
            return False, "已跳过（文件已存在）"
        elif conflict_strategy == "overwrite":
            os.remove(dest_path)
        elif conflict_strategy == "rename":
            dest_path = generate_new_filename(dest_path)
    
    try:
        os.rename(src_path, dest_path)
        return True, ""
    except OSError:
        pass
    
    try:
        src_size = os.path.getsize(src_path)
        shutil.copy2(src_path, dest_path)
        
        dest_size = os.path.getsize(dest_path)
        if src_size != dest_size:
            os.remove(dest_path)
            return False, "文件复制不完整"
        
        os.remove(src_path)
        return True, ""
    except PermissionError:
        return False, "权限错误"
    except FileNotFoundError:
        return False, "文件不存在"
    except OSError as e:
        return False, str(e)

def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    size = size_bytes
    
    while size >= 1024 and index < len(size_names) - 1:
        size /= 1024
        index += 1
    
    return f"{size:.2f} {size_names[index]}"