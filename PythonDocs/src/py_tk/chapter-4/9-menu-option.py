import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

obstr = tk.StringVar()
obstr.set("M1")

ob = ttk.OptionMenu(
    root,
    obstr,
    "M1",
    "M1",
    "M2",
    command=lambda *args: print(args, obstr.get()),
)
ob.pack()

root.mainloop()
