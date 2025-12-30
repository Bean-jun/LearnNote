import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

ttk.Label(root, text="label-1").pack(side=tk.LEFT, expand=True)

# 水平分割线
# separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator = ttk.Separator(root, orient=tk.VERTICAL)
separator.pack(side=tk.LEFT, fill=tk.Y, pady=10)

ttk.Label(root, text="label-2").pack(side=tk.RIGHT, expand=True)


root.mainloop()
