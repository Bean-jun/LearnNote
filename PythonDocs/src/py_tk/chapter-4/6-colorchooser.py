import tkinter as tk
from tkinter import colorchooser, messagebox, ttk

root = tk.Tk()
root.geometry("300x200+100+100")


def handle_click():
    color = colorchooser.askcolor(
        title="Choose color",
    )
    if color:
        print(color)


ttk.Button(
    root,
    text="Click me",
    command=handle_click,
).pack()

root.mainloop()
