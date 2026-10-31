"""Проверки разбора командной строки."""

import unittest

from src.parser import parse_command


class ParserTests(unittest.TestCase):
    """Проверки обычного ввода, кавычек и ошибочного ввода."""

    def test_empty_input(self):
        """Пустая строка не должна создавать команду."""
        self.assertEqual(parse_command("   "), [])

    def test_simple_command(self):
        """Аргументы без кавычек разделяются пробелами."""
        self.assertEqual(parse_command("ls -l /home"), ["ls", "-l", "/home"])

    def test_quoted_arguments(self):
        """Пробелы в кавычках относятся к одному аргументу."""
        self.assertEqual(
            parse_command('cd "Мои документы"'),
            ["cd", "Мои документы"],
        )

    def test_single_quotes(self):
        """Одинарные кавычки также поддерживаются."""
        self.assertEqual(parse_command("ls 'два слова'"), ["ls", "два слова"])

    def test_unclosed_quote(self):
        """Незакрытая кавычка должна вызвать понятную ошибку."""
        with self.assertRaises(ValueError):
            parse_command('cd "папка')


if __name__ == "__main__":
    unittest.main()

