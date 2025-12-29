import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")


def button_click():
    print("Button clicked!")


def button_click2(args):
    print("Button clicked 2!", args)


ttk.Button(root, text="Click me", command=button_click).pack()
# 绑定事件传递参数
ttk.Button(root, text="Click me 2", command=lambda: button_click2("<Click2>")).pack()


root.mainloop()
