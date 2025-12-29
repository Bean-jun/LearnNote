import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

ttk.Label(root, text="Hi, there").pack()

t1 = ttk.Label(root, text="Hi, there")
t1.pack()

t2 = ttk.Label(root)
t2.config(text="Hi, there")
t2.pack()

root.mainloop()
