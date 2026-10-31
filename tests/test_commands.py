"""Проверки команд-заглушек и обработки ошибок."""

import unittest

from src.commands import execute_command


class CommandTests(unittest.TestCase):
    """Проверки результата выполнения команд первого этапа."""

    def test_ls_stub(self):
        """ls выводит имя и переданные аргументы."""
        self.assertEqual(
            execute_command(["ls", "-l"]),
            ("Команда: ls\nАргументы: ['-l']", False),
        )

    def test_cd_stub(self):
        """cd пока только сообщает о своих аргументах."""
        self.assertEqual(
            execute_command(["cd", "Мои документы"]),
            ("Команда: cd\nАргументы: ['Мои документы']", False),
        )

    def test_exit(self):
        """exit сообщает графическому интерфейсу о закрытии."""
        self.assertEqual(execute_command(["exit"]), ("", True))

    def test_exit_with_argument(self):
        """Лишние аргументы для exit считаются ошибкой."""
        self.assertEqual(
            execute_command(["exit", "now"]),
            ("Ошибка: exit не принимает аргументы.", False),
        )

    def test_unknown_command(self):
        """Неизвестная команда возвращает сообщение об ошибке."""
        self.assertEqual(
            execute_command(["unknown"]),
            ("Ошибка: неизвестная команда 'unknown'.", False),
        )

    def test_empty_input(self):
        """Пустой ввод не завершает приложение."""
        self.assertEqual(execute_command([]), ("", False))


if __name__ == "__main__":
    unittest.main()
