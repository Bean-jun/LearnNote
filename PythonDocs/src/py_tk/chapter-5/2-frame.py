import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {"padx": 5, "pady": 5}

        # label
        self.label = ttk.Label(self, text="Hello, Tkinter!")
        self.label.pack(**options)

        # button
        self.button = ttk.Button(self, text="Click Me")
        self.button["command"] = self.button_clicked
        self.button.pack(**options)

        # show the frame on the container
        self.pack(**options)

    def button_clicked(self):
        showinfo(title="Information", message="Hello, Tkinter!")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200+100+100")
        self.title("Simple App")


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    app.mainloop()
