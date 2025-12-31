import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

spinbox_var = tk.StringVar(value=0)

spinbox = ttk.Spinbox(
    root,
    from_=0,
    to=100,
    textvariable=spinbox_var,
    # wrap=True,
    command=lambda: print(spinbox_var.get()),
)
# 禁用微调框
# spinbox["state"] = "disabled"
spinbox.pack()


root.mainloop()
