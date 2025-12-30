import tkinter as tk

root = tk.Tk()
root.geometry("600x400")

label1 = tk.Label(root, text="username:")
entry1 = tk.Entry(root, width=30)
label2 = tk.Label(root, text="password:")
entry2 = tk.Entry(root, width=30, show="*")
btn = tk.Button(root, text="Login")

label1.pack(anchor=tk.W, ipadx=10, padx=10, pady=5)
entry1.pack(anchor=tk.W, fill=tk.X, ipadx=10, padx=20, pady=5)
label2.pack(anchor=tk.W, ipadx=10, padx=10, pady=5)
entry2.pack(anchor=tk.W, fill=tk.X, ipadx=10, padx=20, pady=5)
btn.pack(anchor=tk.W, ipadx=10, padx=20, pady=5)


root.mainloop()
