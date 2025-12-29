import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

entry = ttk.Entry(root, width=30, show="*")
# entry.get()  获取输入框内容
entry.bind("<Return>", lambda event: print(entry.get()))
entry.pack()

# 插入默认文本
# entry.insert(0, "请输入内容")

# 聚焦到输入框
# entry.focus()


# 使用stringVar 绑定输入框内容
entry_var = tk.StringVar()
entry2 = ttk.Entry(root, width=30, textvariable=entry_var)
entry2.pack()

# 绑定标签显示输入框内容
ttk.Label(root, textvariable=entry_var).pack()

# 输入框内容改变时, 标签内容也会改变
entry_var.trace(
    "w", lambda name, index, mode: print(name, index, mode, entry_var.get())
)

print(entry_var.get())

root.mainloop()
