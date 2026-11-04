"""Точка входа для запуска графического эмулятора."""

from src.gui import run_gui
from src.config import parse_config


def main():
    """Запустить эмулятор с переданными настройками."""
    config = parse_config()
    run_gui(config)


if __name__ == "__main__":
    main()