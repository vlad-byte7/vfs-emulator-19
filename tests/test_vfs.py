"""Тестирование виртуальной файловой системы."""

import base64
import tempfile
import unittest

from pathlib import Path
from zipfile import ZipFile, BadZipFile

from src.vfs import load_vfs


def create_test_zip(folder, contents):
    """Создать временный ZIP-архив с заданными файлами."""
    zip_path = Path(folder) / "test.zip"

    with ZipFile(zip_path, "w") as archive:
        for name, content in contents.items():
            archive.writestr(name, content)

    return zip_path


class VFSTests(unittest.TestCase):
    
    def test_missing_archive(self):
        """Проверить загрузку несуществующего архива."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.zip"

            with self.assertRaises(FileNotFoundError):
                load_vfs(path)

    def test_invalid_archive(self):
        """Проверить файл, который не является ZIP."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.zip"

            path.write_text(
                "This is not a ZIP archive",
                encoding="utf-8"
            )

            with self.assertRaises(BadZipFile):
                load_vfs(path)

    def test_invalid_path(self):
        """Проверить отклонение некорректного пути."""
        with tempfile.TemporaryDirectory() as folder:
            path = create_test_zip(
                folder,
                {"../secret.txt": "Secret"}
            )

            with self.assertRaises(ValueError):
                load_vfs(path)

    def test_minimal_zip(self):
        """Проверить архив с одним файлом."""
        with tempfile.TemporaryDirectory() as folder:
            path = create_test_zip(
                folder,
                {"readme.txt": "Hello"}
            )

            directories, files = load_vfs(path)

            self.assertEqual(directories, {"/"})
            self.assertIn("/readme.txt", files)

    def test_multiple_files(self):
        """Проверить архив с несколькими файлами."""
        with tempfile.TemporaryDirectory() as folder:
            path = create_test_zip(
                folder,
                {
                    "a.txt": "A",
                    "b.txt": "B",
                    "c.txt": "C"
                }
            )

            directories, files = load_vfs(path)

            self.assertEqual(len(files), 3)
            self.assertEqual(directories, {"/"})

    def test_nested_folders(self):
        """Проверить вложенные папки."""
        with tempfile.TemporaryDirectory() as folder:
            path = create_test_zip(
                folder,
                {
                    "projects/python/app/src/main.py": "print(42)"
                }
            )

            directories, files = load_vfs(path)

            self.assertIn("/projects", directories)
            self.assertIn("/projects/python", directories)
            self.assertIn("/projects/python/app", directories)
            self.assertIn("/projects/python/app/src", directories)
            self.assertIn(
                "/projects/python/app/src/main.py",
                files
            )

            self.assertFalse(
                (Path(folder) / "projects").exists()
            )

    def test_binary_data(self):
        """Проверить сохранение двоичных данных."""
        binary = bytes([0, 255, 128, 1])

        with tempfile.TemporaryDirectory() as folder:
            path = create_test_zip(
                folder,
                {"image.bin": binary}
            )

            directories, files = load_vfs(path)

            decoded = base64.b64decode(files["/image.bin"])

            self.assertEqual(decoded, binary)