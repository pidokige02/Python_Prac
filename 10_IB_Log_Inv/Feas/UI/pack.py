import tkinter as tk

root = tk.Tk()

button1 = tk.Button(root, text="Button 1")
button1.pack(side="top", fill="x")

button2 = tk.Button(root, text="Button 2")
button2.pack(side="left", fill="y")

button3 = tk.Button(root, text="Button 3")
button3.pack(side="right", fill="y")

root.mainloop()
