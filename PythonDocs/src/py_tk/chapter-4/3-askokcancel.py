import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.geometry("300x200+100+100")


def handle_click():
    answer = messagebox.askokcancel(
        "Info",
        "Hello from py-tk!",
    )
    if answer:
        print("OK")
    else:
        print("Cancel")


ttk.Button(
    root,
    text="Click me",
    command=handle_click,
).pack()

root.mainloop()
