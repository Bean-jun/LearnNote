import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.geometry("300x200+100+100")

ttk.Button(
    root,
    text="INFO",
    command=lambda: messagebox.showinfo(
        "Info",
        "Hello from py-tk!",
    ),
).pack()
ttk.Button(
    root,
    text="WARNING",
    command=lambda: messagebox.showwarning(
        "WARNING",
        "Hello from py-tk!",
    ),
).pack()
ttk.Button(
    root,
    text="ERROR",
    command=lambda: messagebox.showerror(
        "ERROR",
        "Hello from py-tk!",
    ),
).pack()

root.mainloop()
