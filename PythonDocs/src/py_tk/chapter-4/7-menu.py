import tkinter as tk
from tkinter import Menu

root = tk.Tk()
root.geometry("300x200+100+100")

# 初始化菜单
menu_bar = Menu(root)
# 添加菜单到root
root.config(menu=menu_bar)

# 添加菜单选项
menu_bar.add_command(
    label="M1",
    command=lambda: print("M1"),
)
menu_bar.add_command(
    label="M2",
    command=lambda: print("M2"),
)

# 添加子菜单
# 初始化子菜单
sub_menu = Menu(menu_bar, tearoff=0)
# 添加子菜单到主菜单
menu_bar.add_cascade(label="M3", menu=sub_menu)
# 添加子菜单选项
sub_menu.add_command(label="S1", command=lambda: print("S1"))
# 添加分隔线
sub_menu.add_separator()
sub_menu.add_command(label="S2", command=lambda: print("S2"))

# 添加子菜单选项
sub_menu_options = Menu(sub_menu, tearoff=0)
# 添加子菜单选项到子菜单
sub_menu.add_cascade(label="Options", menu=sub_menu_options)
# 添加子菜单选项到子菜单选项
sub_menu_options.add_command(label="O1", command=lambda: print("O1"))
sub_menu_options.add_command(label="O2", command=lambda: print("O2"))


root.mainloop()
