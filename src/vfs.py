"""Виртуальная файловая система на основе ZIP-архива."""

import base64
from zipfile import ZipFile


def load_vfs(zip_path):
    """Загрузить файлы и папки ZIP-архива в память."""
    directories = {"/"}
    files = {}

    with ZipFile(zip_path, "r") as archive:
        for entry in archive.infolist():
            raw_path = entry.filename
            path = raw_path.strip("/")

            if not path:
                continue

            parts = path.split("/")

            if raw_path.startswith("/") or "\\" in raw_path:
                raise ValueError("Некорректный путь в ZIP")

            if any(part in ("", ".", "..") for part in parts):
                raise ValueError("Некорректный путь в ZIP")

            for index in range(1, len(parts)):
                folder = "/" + "/".join(parts[:index])
                directories.add(folder)

            virtual_path = "/" + path

            if entry.is_dir():
                directories.add(virtual_path)
            else:
                content = archive.read(entry)
                encoded = base64.b64encode(content).decode("ascii")
                files[virtual_path] = encoded

    return directories, files