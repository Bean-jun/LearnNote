import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x300")
root.title("Tkinter Top Level Example")


def open_top_level_window():
    window = tk.Toplevel(root)
    window.geometry("200x200")
    window.title("Top Level Window")
    # 禁止主窗口接收事件
    window.grab_set()
    ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)


ttk.Button(root, text="Open Top Level Window", command=open_top_level_window).pack()

root.mainloop()
