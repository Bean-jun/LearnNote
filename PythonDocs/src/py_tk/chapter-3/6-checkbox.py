import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

agreement_var = tk.StringVar()

checkbox = ttk.Checkbutton(
    root,
    text="Check me",
    offvalue="OFF",
    onvalue="ON",
    variable=agreement_var,
    command=lambda: print(agreement_var.get()),
)

checkbox.pack()

root.mainloop()
