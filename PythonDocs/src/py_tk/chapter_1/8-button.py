import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.geometry("300x200+100+100")

# 按钮
img = tk.PhotoImage(file="./assets/img-1.png")
btn = ttk.Button(
    root,
    text="Click me!",
    image=img,
    compound="top",
)
# 按钮状态
btn.config(state="normal")
btn.config(command=lambda: messagebox.showinfo("Info", "Button clicked!"))
btn.pack()


root.mainloop()
