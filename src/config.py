"""Обработка параметров запуска эмулятора."""

import argparse


def parse_config(argv=None):
    """Получить настройки из командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки VFS"
    )

    parser.add_argument(
        "--vfs",
        help="Путь к виртуальной файловой системе"
    )

    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту"
    )

    return parser.parse_args(argv)