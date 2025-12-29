# tkinter 快速入门

## 1. quick start

### 1.1 窗口属性
- 使用 title（） 方法更改窗口标题。
- 使用 geometry（） 方法来更改窗口的大小和位置。
- 使用 resizable（） 方法来指定窗口是可以水平调整大小还是垂直调整大小。
- 使用 window.attributes('-alpha',0.5) 设置窗口的透明度。
- 使用 window.attributes('-topmost', 1) 让窗户始终在顶部。
- 使用 lift（） 和 lower（） 方法将窗口上下移动。
- 使用 iconbitmap（） 方法更改窗口的默认图标。

### 1.2 widget

tk 和 ttk 小部件又有哪些区别？

tk 小部件是传统的 Tkinter 小部件，而 ttk 小部件是基于主题的小部件。

```shell
Button
Checkbutton
Entry
Frame
Label
LabelFrame
Menubutton
PanedWindow
Radiobutton
Scale
Scrollbar
Spinbox

# And the following widgets are new and specific to ttk:
Combobox
Notebook
Progressbar
Separator
Sizegrip
Treeview
```

Tkinter 既有经典款，也有主题小工具（ttk 小工具）。Tk 主题的小部件也被称为 ttk 小部件。

### 1.3 command bind 命令绑定

在 Tkinter 中，为控件的命令选项分配函数名称称为命令绑定。当对应事件发生时，分配的函数将自动调用。

只有少数小部件支持命令选项。

### 1.4 event bind 事件绑定

绑定事件处理函数
`widget.bind(event, handler, add=None)`

解绑事件处理函数
`widget.unbind(event)`

### 1.5 标签显示图片

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")


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
```

### 1.6 按钮显示图片
```python
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
```

### 1.7 输入框

用 `ttk.Entry` 用于创建文本框的入口小工具。
通过 `StringVar` 对象跟踪并更改 Entry 控件的当前值。

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

entry = ttk.Entry(root, width=30, show="*")
# entry.get()  获取输入框内容
entry.bind("<Return>", lambda event: print(entry.get()))
entry.pack()

# 插入默认文本
# entry.insert(0, "请输入内容")

# 聚焦到输入框
# entry.focus()


# 使用stringVar 绑定输入框内容
entry_var = tk.StringVar()
entry2 = ttk.Entry(root, width=30, textvariable=entry_var)
entry2.pack()

# 绑定标签显示输入框内容
ttk.Label(root, textvariable=entry_var).pack()

# 输入框内容改变时, 标签内容也会改变
entry_var.trace(
    "w", lambda name, index, mode: print(name, index, mode, entry_var.get())
)

print(entry_var.get())

root.mainloop()
```