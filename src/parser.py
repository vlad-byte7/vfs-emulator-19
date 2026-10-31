"""Разбор текстовых команд с корректной обработкой кавычек."""

import shlex


def parse_command(line):
    """Разбить введённую строку на команду и её аргументы."""
    return shlex.split(line, posix=True)

