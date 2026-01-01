import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.geometry("300x200+100+100")

# 样式
style = ttk.Style(root)

# 设置主题
style.theme_use("xpnative")

# 获取所有的主题
print(style.theme_names())

ttk.Button(root, text="Click me!").grid(row=0, column=0)

root.mainloop()
