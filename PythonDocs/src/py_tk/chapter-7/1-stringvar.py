import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")
strs = tk.StringVar()

ttk.Label(root, textvariable=strs).pack(fill=tk.X)
ttk.Entry(root, textvariable=strs).pack(fill=tk.X)

root.mainloop()
