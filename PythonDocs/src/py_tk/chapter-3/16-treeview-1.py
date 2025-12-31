import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")
root.title("Tkinter Treeview")

# 创建树视图
treeview = ttk.Treeview()
# 插入一级项目
level1 = treeview.insert("", tk.END, text="San Jose")
# 插入二级项目
treeview.insert(level1, tk.END, text="John Doe")
treeview.insert(level1, tk.END, text="Jane Doe")

treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
root.mainloop()
