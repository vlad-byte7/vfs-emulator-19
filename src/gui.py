"""Простой графический терминал на базе стандартного Tkinter."""

import tkinter as tk

from src.commands import execute_command
from src.parser import parse_command


def append_output(output, message):
    """Добавить текст в терминал и прокрутить его вниз."""
    output.configure(state="normal")
    output.insert("end", message + "\n")
    output.see("end")
    output.configure(state="disabled")


def handle_input(root, output, entry):
    """Обработать строку из поля ввода после нажатия Enter."""
    line = entry.get()
    entry.delete(0, "end")
    append_output(output, f"vfs:/$ {line}")

    try:
        parts = parse_command(line)
    except ValueError as error:
        append_output(output, f"Ошибка разбора: {error}")
        return

    result, should_exit = execute_command(parts)
    if result:
        append_output(output, result)
    if should_exit:
        root.destroy()


def run_gui():
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

    append_output(output, "VFS — этап 1 (REPL)")
    append_output(output, "Команды: ls, cd, exit")
    entry.focus_set()
    root.mainloop()

