"""Тесты стартовых скриптов."""

import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from src.gui import run_startup_script
from src.script_runner import read_script


class ScriptTests(unittest.TestCase):

    def test_read_script(self):
        """Проверить чтение команд и пропуск пустых строк."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "startup.txt"
            path.write_text(
                'ls\n\ncd "Мои документы"\n',
                encoding="utf-8"
            )

            commands = read_script(path)

        self.assertEqual(
            commands,
            ["ls", 'cd "Мои документы"']
        )

    def test_missing_script(self):
        """Проверить ошибку отсутствующего файла."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.txt"

            with self.assertRaises(FileNotFoundError):
                read_script(path)

    def test_stop_on_first_error(self):
        """Проверить остановку после ошибочной команды."""
        commands = ["ls", "unknown", "cd documents"]

        with patch("src.gui.read_script", return_value=commands):
            with patch(
                "src.gui.execute_line",
                side_effect=[False, True]
            ) as execute_mock:
                run_startup_script(None, None, "startup.txt")

        self.assertEqual(execute_mock.call_count, 2)