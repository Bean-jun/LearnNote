import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")
# 设置光标为watch,忙碌状态
root.config(cursor="")


def handler_click():
    root.config(cursor="watch")
    btn.config(cursor="watch")


btn = ttk.Button(
    root,
    text="Click me",
    cursor="arrow",
    command=handler_click,
)
btn.pack()

root.mainloop()
