import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

# 按钮
btn = ttk.Button(root, text="Click me!")
btn.grid(row=0, column=0)

# 标签
label = ttk.Label(root, text="Hello, Tkinter!")
label.grid(row=1, column=0)

root.mainloop()
