import tkinter as tk
from tkinter.scrolledtext import ScrolledText

stext = ScrolledText(bg="white", height=10)
stext.insert(tk.END, "__doc__\n" * 20)
stext.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
stext.focus_set()
stext.mainloop()
