import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

# style = ttk.Style()
# style.theme_use("classic")


pw = ttk.PanedWindow(root, orient=tk.HORIZONTAL)

listbox1 = tk.Listbox(root)
pw.add(listbox1)
listbox2 = tk.Listbox(root)
pw.add(listbox2)

pw.pack()

root.mainloop()
