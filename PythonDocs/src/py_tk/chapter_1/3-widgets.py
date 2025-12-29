import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

# 经典label & 新label
tk.Button(root, text="Hello from py-tk!").pack()
ttk.Button(root, text="Hello from py-tk!").pack()

tk.Checkbutton(root, text="Hello from py-tk!").pack()
ttk.Checkbutton(root, text="Hello from py-tk!").pack()

tk.Entry(root, text="Hello from py-tk!").pack()
ttk.Entry(root, text="Hello from py-tk!").pack()

root.mainloop()
