"""Команды-заглушки и завершение работы эмулятора."""


def execute_command(parts):
    """Вернуть текст ответа и признак необходимости завершить работу."""
    if not parts:
        return "", False

    command, *arguments = parts

    if command in ("ls", "cd"):
        result = f"Команда: {command}\nАргументы: {arguments}"
        return result, False

    if command == "exit":
        if arguments:
            return "Ошибка: exit не принимает аргументы.", False
        return "", True

    return f"Ошибка: неизвестная команда '{command}'.", False

