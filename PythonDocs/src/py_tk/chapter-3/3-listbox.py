import tkinter as tk
from tkinter.messagebox import showinfo


def handle_item_select(event):
    selected_indices = listbox.curselection()
    selected_languages = ",".join([listbox.get(i) for i in selected_indices])
    print(event)
    showinfo(title="Information", message=f"You selected: {selected_languages}")


root = tk.Tk()
root.geometry("300x200+100+100")

items = ["Item 1", "Item 2", "Item 3", "Item 4"]
list_items = tk.Variable(value=items)

listbox = tk.Listbox(
    root,
    listvariable=list_items,
    selectmode=tk.SINGLE,
)

listbox.bind("<<ListboxSelect>>", handle_item_select)
listbox.pack()


root.mainloop()
