"""Простой графический терминал на базе стандартного Tkinter."""

import tkinter as tk

from src.commands import execute_command
from src.parser import parse_command
from src.script_runner import read_script
from zipfile import BadZipFile
from src.vfs import load_vfs

def append_output(output, message):
    """Добавить текст в терминал и прокрутить его вниз."""
    output.configure(state="normal")
    output.insert("end", message + "\n")
    output.see("end")
    output.configure(state="disabled")

def execute_line(root, output, line):
    """Выполнить команду и сообщить, нужно ли остановиться."""
    append_output(output, f"vfs:/$ {line}")

    try:
        parts = parse_command(line)
    except ValueError as error:
        append_output(output, f"Ошибка разбора: {error}")
        return True

    result, should_exit = execute_command(parts)

    if result:
        append_output(output, result)

    if should_exit:
        root.destroy()

    return should_exit or result.startswith("Ошибка:")

def handle_input(root, output, entry):
    """Обработать ввод команды пользователем."""
    line = entry.get()
    entry.delete(0, "end")

    execute_line(root, output, line)


def run_startup_script(root, output, path):
    """Выполнить команды стартового скрипта до первой ошибки."""
    try:
        commands = read_script(path)
    except OSError as error:
        append_output(output, f"Ошибка чтения скрипта: {error}")
        return

    for line in commands:
        stop = execute_line(root, output, line)

        if stop:
            break

def mount_vfs(root, output, path):
    """Загрузить виртуальную файловую систему в память."""
    if not path:
        return

    try:
        directories, files = load_vfs(path)
    except (OSError, BadZipFile, ValueError) as error:
        append_output(output, f"Ошибка загрузки VFS: {error}")
        return

    root.vfs = (directories, files)

    append_output(
        output,
        f"VFS загружена: {len(directories)} папок, {len(files)} файлов"
    )

def run_gui(config):
    """Создать окно терминала и запустить цикл событий Tkinter."""
    root = tk.Tk()
    root.title("VFS — эмулятор командной строки")
    root.geometry("760x480")
    root.minsize(560, 340)
    root.configure(bg="#15202b")

    output = tk.Text(
        root, bg="#101820", fg="#d8e5ed", insertbackground="white",
        font=("Consolas", 11), padx=12, pady=12, wrap="word",
        relief="flat", state="disabled",
    )
    output.pack(fill="both", expand=True, padx=12, pady=(12, 4))

    input_frame = tk.Frame(root, bg="#15202b")
    input_frame.pack(fill="x", padx=12, pady=(4, 12))
    tk.Label(
        input_frame, text="vfs:/$", bg="#15202b", fg="#88e5ac",
        font=("Consolas", 11),
    ).pack(side="left")
    entry = tk.Entry(
        input_frame, bg="#233446", fg="white", insertbackground="white",
        font=("Consolas", 11), relief="flat",
    )
    entry.pack(side="left", fill="x", expand=True, padx=(8, 0), ipady=7)
    entry.bind("<Return>", lambda event: handle_input(root, output, entry))

    append_output(output, "VFS — этап 2 (Конфигурация)")
    append_output(output, "Команды: ls, cd, exit")

    append_output(output, f"Путь к VFS: {config.vfs or 'Не указан'}")
    append_output(output, f"Стартовый скрипт: {config.script or 'Не указан'}")

    root.vfs = None
    mount_vfs(root, output, config.vfs)

    if config.script:
        root.after( 0, lambda: run_startup_script(root, output, config.script) )

    entry.focus_set()
    root.mainloop()

