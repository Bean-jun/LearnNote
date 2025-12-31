import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

sizegrip = ttk.Sizegrip(root)
sizegrip.pack(side=tk.BOTTOM, anchor=tk.SE)

root.mainloop()
