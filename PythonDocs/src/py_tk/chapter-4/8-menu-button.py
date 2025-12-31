import tkinter as tk
from tkinter import Menu, ttk

root = tk.Tk()
root.geometry("300x200+100+100")

mb = ttk.Menubutton(root, text="Menu Button")
mb.pack()

# 初始化菜单
menu_bar = Menu(mb, tearoff=0)
# 添加菜单到root
mb.config(menu=menu_bar)

# 添加菜单选项
menu_bar.add_command(
    label="M1",
    command=lambda: print("M1"),
)
menu_bar.add_command(
    label="M2",
    command=lambda: print("M2"),
)


root.mainloop()
