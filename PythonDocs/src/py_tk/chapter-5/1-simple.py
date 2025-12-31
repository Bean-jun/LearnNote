import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200+100+100")
        self.title("Simple App")
        # 按钮
        btn = ttk.Button(self, text="Click me!")
        btn.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
