"""Тесты обработки параметров запуска."""

import unittest

from src.config import parse_config


class ConfigTests(unittest.TestCase):

    def test_no_arguments(self):
        """Проверить запуск без параметров."""
        config = parse_config([])

        self.assertIsNone(config.vfs)
        self.assertIsNone(config.script)

    def test_both_arguments(self):
        """Проверить оба параметра запуска."""
        config = parse_config([
            "--vfs", "filesystem.zip",
            "--script", "startup.txt"
        ])

        self.assertEqual(config.vfs, "filesystem.zip")
        self.assertEqual(config.script, "startup.txt")

    def test_only_vfs(self):
        """Проверить запуск только с путём VFS."""
        config = parse_config(["--vfs", "test.zip"])

        self.assertEqual(config.vfs, "test.zip")
        self.assertIsNone(config.script)