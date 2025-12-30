import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry("300x200")

scrollbar = ttk.Scrollbar(root, orient="vertical")
scrollbar.pack(side="right", fill="y")

text = tk.Text(root, height=8, insertbackground="red")
text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
text.insert(tk.END, "1-1\n" * 30)

# 配置text的垂直滚动条
# 通过将 scrollbar.set 方法分配给文本控件的 yscrollcommand，并将文本控件的 text.yview 映射到滚动条控件的命令中，将卷轴小部件关联起来
text.config(yscrollcommand=scrollbar.set)
# 配置滚动条的命令
scrollbar.config(command=text.yview)

root.mainloop()
