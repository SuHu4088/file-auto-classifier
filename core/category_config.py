EXTENSION_CATEGORIES = {
    "视频": [
        "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm",
        "m4v", "mpeg", "mpg", "3gp", "ogg", "ogv", "rm", "rmvb"
    ],
    "图片": [
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp",
        "svg", "ico", "heic", "heif", "raw", "cr2", "nef", "dng"
    ],
    "文本": [
        "txt", "md", "doc", "docx", "pdf", "xlsx", "xls",
        "pptx", "ppt", "csv", "rtf", "odt", "ods", "odp",
        "pages", "numbers", "key", "epub", "mobi", "chm"
    ],
    "音频": [
        "mp3", "wav", "flac", "aac", "ogg", "wma", "m4a",
        "alac", "ape", "opus", "dsd", "dff", "dsf"
    ],
    "压缩": [
        "zip", "rar", "7z", "tar", "gz", "bz2", "xz",
        "iso", "cab", "arj", "lzh", "z", "deb", "rpm"
    ],
    "安装包": [
        "exe", "msi", "apk", "dmg", "pkg", "app", "deb", "rpm"
    ],
    "代码": [
        "py", "js", "ts", "html", "css", "java", "cpp", "c",
        "h", "hpp", "go", "rs", "php", "ruby", "rb", "swift",
        "kotlin", "kt", "scala", "sql", "json", "yaml", "yml",
        "xml", "toml", "ini", "cfg", "conf"
    ],
    "程序": [
        "dll", "so", "dylib", "sys", "drv", "bat", "cmd",
        "sh", "ps1", "vbs", "wsf", "scr", "lnk"
    ],
    "数据库": [
        "db", "sqlite", "mdb", "accdb", "sql", "bak", "dump"
    ],
    "其他": []
}

CATEGORY_COLORS = {
    "视频": "#FF6B6B",
    "图片": "#4ECDC4",
    "文本": "#FFE66D",
    "音频": "#95E1D3",
    "压缩": "#A29BFE",
    "安装包": "#FD79A8",
    "代码": "#74B9FF",
    "程序": "#55EFC4",
    "数据库": "#FDcb6E",
    "其他": "#636E72"
}

def get_category(extension):
    ext = extension.lower().strip('.')
    for category, extensions in EXTENSION_CATEGORIES.items():
        if ext in extensions:
            return category
    return "其他"

def get_category_color(category):
    return CATEGORY_COLORS.get(category, "#636E72")