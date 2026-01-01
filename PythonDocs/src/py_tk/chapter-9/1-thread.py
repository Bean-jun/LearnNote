import threading
import time
import tkinter as tk
from tkinter import ttk


def task():
    # Simulate a long-running task
    for i in range(5):
        print(f"Task running... {i+1}/5")
        time.sleep(1)

    print("Task completed!")


def handler_thread():
    thread = threading.Thread(target=task)
    thread.start()


root = tk.Tk()
root.geometry("300x300")
root.title("Tkinter Thread Example")

button = ttk.Button(root, text="Start no Thread", command=task)
button.pack(pady=10)
btn1 = ttk.Button(root, text="Start Thread", command=handler_thread)
btn1.pack(pady=10)
btn2 = ttk.Button(root, text="click me", command=lambda: print("click me"))
btn2.pack(pady=10)

root.mainloop()
