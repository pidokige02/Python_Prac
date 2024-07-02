import tkinter as tk
from tkinter import ttk

def on_ok():
    print(f"Name: {name_entry.get()}")
    print(f"Customer: {customer_var.get()}")
    root.destroy()

def on_cancel():
    root.destroy()

root = tk.Tk()
root.title("Enter values")

# Set window size
root.geometry("300x150")

# Name label and entry
name_label = ttk.Label(root, text="Name")
name_label.pack(pady=(10, 0))

name_entry = ttk.Entry(root)
name_entry.pack(pady=(0, 10), padx=10, fill='x')

# Customer label and dropdown
customer_label = ttk.Label(root, text="Customer")
customer_label.pack(pady=(10, 0))

customer_var = tk.StringVar()
customer_dropdown = ttk.Combobox(root, textvariable=customer_var)
customer_dropdown['values'] = ("Customer1", "Customer2", "Customer3")  # Example values
customer_dropdown.pack(pady=(0, 10), padx=10, fill='x')

# OK and Cancel buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=(10, 0))

ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
ok_button.pack(side="left", padx=(0, 5))

cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
cancel_button.pack(side="left", padx=(5, 0))

root.mainloop()
