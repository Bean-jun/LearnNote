import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

notebook = ttk.Notebook(root)
notebook.pack()

frame1 = ttk.Frame(notebook, width=300, height=200)
notebook.add(frame1, text="Tab 1")

frame2 = ttk.Frame(notebook, width=300, height=200)
notebook.add(frame2, text="Tab 2")

frame3 = ttk.Frame(notebook, width=300, height=200)
notebook.add(frame3, text="Tab 3")

# 选择第二个选项卡
notebook.select(frame2)

# 获取当前选择的选项卡
current_tab = notebook.select()
print(current_tab)

# 隐藏第一个选项卡
notebook.hide(frame1)

# 移除第一个选项卡
notebook.forget(frame1)

root.mainloop()
