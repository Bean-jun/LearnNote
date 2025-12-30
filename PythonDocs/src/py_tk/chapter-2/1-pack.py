import tkinter as tk

root = tk.Tk()
root.title("Tkinter Pack Layout")
root.geometry("600x400")

label1 = tk.Label(root, text="Tkinter", bg="red", fg="white")
label2 = tk.Label(root, text="Pack Layout", bg="green", fg="white")
label3 = tk.Label(root, text="Demo", bg="blue", fg="white")

label1.pack(side=tk.TOP, expand=True, fill=tk.X, ipadx=10, ipady=20, padx=20)
label2.pack(side=tk.TOP, expand=True, fill=tk.X, ipadx=10, ipady=20, padx=20)
label3.pack(side=tk.TOP, expand=True, fill=tk.X, ipadx=10, ipady=20, padx=20)

root.mainloop()
