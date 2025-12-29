import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")


t = ttk.Label(root, text="Hello from py-tk!")
# 绑定事件传递参数
t.bind("<Button-1>", lambda event: print("Label clicked-1!", event))
t.bind("<Button-3>", lambda event: print("Label clicked-2!", event), add="+")
t.pack()

root.mainloop()
