import tkinter as tk

root = tk.Tk()
root.geometry("300x300")


root.after(1000, lambda: print("after 1 second"))

root.mainloop()
