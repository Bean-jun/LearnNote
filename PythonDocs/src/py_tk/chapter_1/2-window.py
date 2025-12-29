import tkinter as tk

root = tk.Tk()
# 设置窗口标题
root.title("Hello from py-tk!")
# 设置窗口大小和位置, 300x200 窗口大小, 左100下100 窗口位置
root.geometry("300x200+100+100")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f"屏幕宽度: {screen_width}")
print(f"屏幕高度: {screen_height}")

# 居中窗口
window_width = 300
window_height = 200
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 禁用窗口最大化按钮
# root.resizable(False, True)

# 设置窗口最小和最大尺寸
root.minsize(200, 200)
root.maxsize(400, 400)

# 设置窗口透明度
root.attributes("-alpha", 0.9)

# 设置窗口置顶
root.attributes("-topmost", True)

# 设置窗口图标
root.iconbitmap("./pygame.ico")

root.mainloop()
