import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

selector_var = tk.StringVar()

combo = ttk.Combobox(
    root,
    textvariable=selector_var,
    values=["Option 1", "Option 2", "Option 3"],
)
# 只读状态，用户只能选择已有的选项，不能输入自定义值
combo["state"] = "readonly"
combo.bind("<<ComboboxSelected>>", lambda event: print(selector_var.get()))
combo.pack()


root.mainloop()
