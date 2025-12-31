import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200+100+100")

progressbar = ttk.Progressbar(
    root,
    orient=tk.HORIZONTAL,
    length=100,
    mode="determinate",
)
progressbar.pack()


def start_progress():
    progressbar.start()
    val = progressbar["value"]
    progress_label.config(text=f"Progress: {val}%")


progress_label = ttk.Label(root, text="Progress: 0%")
progress_label.pack()

btn = ttk.Button(root, text="Start", command=start_progress)
btn.pack()


root.mainloop()
