import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("帧切换示例")
        self.geometry("400x300")

        # 1. 创建父容器（所有Frame的共同父级）
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)  # 占满主窗口

        # 2. 定义所有需要切换的Frame
        self.frames = {}  # 存储Frame实例，方便调用
        for F in (HomePage, SettingsPage):
            frame = F(self.container, self)  # 父容器是self.container
            self.frames[F] = frame
            # 关键：所有Frame用grid布局重叠（row=0, column=0，占满父容器）
            frame.grid(row=0, column=0, sticky="nsew")

        # 3. 初始显示首页
        self.show_frame(HomePage)

    def show_frame(self, frame_class):
        """切换到指定Frame的方法"""
        frame = self.frames[frame_class]
        frame.tkraise()  # 核心：将目标Frame提升到最上层


# 定义首页Frame
class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # controller是主App实例，用于调用show_frame切换页面
        self.controller = controller

        # 首页控件
        ttk.Label(self, text="首页").pack(pady=50)
        # 切换到设置页的按钮
        ttk.Button(
            self,
            text="进入设置页",
            command=lambda: self.controller.show_frame(SettingsPage),
        ).pack(pady=20)


# 定义设置页Frame
class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 设置页控件
        ttk.Label(self, text="设置页").pack(pady=50)
        # 切换回首页的按钮
        ttk.Button(
            self, text="返回首页", command=lambda: self.controller.show_frame(HomePage)
        ).pack(pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
