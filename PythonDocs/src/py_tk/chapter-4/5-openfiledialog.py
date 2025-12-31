import tkinter as tk
from tkinter import filedialog, messagebox, ttk

root = tk.Tk()
root.geometry("300x200+100+100")


def handle_click():
    filename = filedialog.askopenfilename(
        title="Open file",
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ],
    )
    if filename:
        print(filename)


ttk.Button(
    root,
    text="Click me",
    command=handle_click,
).pack()

root.mainloop()
