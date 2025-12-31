import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")
root.title("Tkinter Treeview")

# 创建树视图
treeview = ttk.Treeview(columns=("Name", "Number"))
# 设置列标题
treeview.heading("#0", text="City")
treeview.heading("Name", text="Name")
treeview.heading("Number", text="Number")


# 插入一级项目
level1 = treeview.insert("", tk.END, text="湖北", open=True)
# 插入二级项目
treeview.insert(level1, tk.END, text="武汉", values=("100000",))
treeview.insert(level1, tk.END, text="荆州", values=("100001",))
treeview.insert(level1, tk.END, text="宜昌", values=("100002",))
treeview.insert(level1, tk.END, text="黄石", values=("100003",))

treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
root.mainloop()
