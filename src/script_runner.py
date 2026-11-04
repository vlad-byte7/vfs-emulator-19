"""Чтение стартового скрипта."""

def read_script(path):
    """Прочитать команды из текстового файла."""
    commands = []

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        command = line.strip()

        if command:
            commands.append(command)

    return commands