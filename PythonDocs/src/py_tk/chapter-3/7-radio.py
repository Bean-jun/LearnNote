import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

selector_var = tk.StringVar()

r1 = ttk.Radiobutton(
    root,
    text="Check me - 1",
    value="1",
    variable=selector_var,
    command=lambda: print(selector_var.get()),
)
r2 = ttk.Radiobutton(
    root,
    text="Check me - 2",
    value="2",
    variable=selector_var,
    command=lambda: print(selector_var.get()),
)
r1.pack()
r2.pack()


root.mainloop()
