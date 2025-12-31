import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

labelframe = ttk.LabelFrame(
    root,
    text="Frame Title",
    height=150,
    width=150,
    padding=10,
)
labelframe.pack(padx=10, pady=10)

checkbox = ttk.Checkbutton(labelframe, text="Check me")
checkbox.pack()

root.mainloop()
