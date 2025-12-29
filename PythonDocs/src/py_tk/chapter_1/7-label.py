import tkinter as tk
from tkinter import ttk

root = tk.Tk()
# root.geometry("300x200+100+100")


# 标签显示图片
img = tk.PhotoImage(file="./assets/img-1.png")
ttk.Label(
    root,
    text="http & websocket",
    font=("微软雅黑", 18),
    image=img,
    compound="top",
).pack()

root.mainloop()
