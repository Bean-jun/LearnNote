import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

scroller = ttk.Scrollbar(root, orient=tk.VERTICAL)
scroller.pack(side=tk.RIGHT, fill=tk.Y)

items = [f"Item {i}" for i in range(100)]
list_items = tk.Variable(value=items)

listbox = tk.Listbox(
    root,
    listvariable=list_items,
    selectmode=tk.SINGLE,
)
listbox.config(yscrollcommand=scroller.set)
scroller.config(command=listbox.yview)
listbox.pack(fill=tk.BOTH)


root.mainloop()
