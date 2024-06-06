import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
print(f"Width: {width}, Height: {height}")
root.destroy()


# from screeninfo import get_monitors

# for monitor in get_monitors():
#     print(f"Width: {monitor.width}, Height: {monitor.height}, Name: {monitor.name}")
