import tkinter as tk

root = tk.Tk()

root.geometry("400x300")
canvas = tk.Canvas(root, width=600, height=400, bg="white")

a = canvas.create_line(100, 100, 200, 200, fill="red")
b = canvas.create_rectangle(100, 100, 150, 150, fill="blue")

# 绑定事件&canvas.delete用来删除对应标记原始
canvas.tag_bind(b, "<Button-1>", lambda e: canvas.delete(a))

canvas.pack()

root.mainloop()
