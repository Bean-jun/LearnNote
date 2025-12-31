import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

slider_var = tk.DoubleVar()


slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    variable=slider_var,
    orient=tk.HORIZONTAL,
    # orient=tk.VERTICAL,
    command=lambda event: print(slider_var.get()),
)
# 禁用滑动条
# slider["state"] = "disabled"
slider.pack()


root.mainloop()
