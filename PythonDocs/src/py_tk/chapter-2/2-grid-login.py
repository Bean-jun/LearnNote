import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

# grid 3x2
# 使用 rowconfigure（） 和 columnconfigure（） 方法设置一个由 3 行 2 列组成的网格
# 使用 columnconfigure（） 和 rowconfigure（） 方法来指定网格列和行的权重
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

label1 = ttk.Label(root, text="username:")
label1.grid(row=0, column=0, pady=10)
entry1 = ttk.Entry(root, width=30)
entry1.grid(row=0, column=1)

label2 = ttk.Label(root, text="password:")
label2.grid(row=1, column=0, pady=10)
entry2 = ttk.Entry(root, width=30, show="*")
entry2.grid(row=1, column=1)

btn = ttk.Button(root, text="Login")
btn.grid(row=2, column=1, sticky=tk.E, pady=10)


root.mainloop()
