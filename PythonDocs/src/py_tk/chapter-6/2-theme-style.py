import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.geometry("300x200+100+100")

btn = ttk.Button(root, text="Click me!")
btn.grid(row=0, column=0)

# 获取按钮的样式类 TButton
print(btn.winfo_class())

style = ttk.Style(root)
# 更新TButton的样式
style.configure("TButton", font=("fire code", 12))

# 获取TButton的布局
print(style.layout("TButton"))

root.mainloop()
