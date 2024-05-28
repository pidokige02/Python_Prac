import tkinter as tk
from tkinter import filedialog, Text

def open_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        content = file.read()
        text_widget.insert(tk.END, content)

root = tk.Tk()
root.title("File Viewer")

text_widget = Text(root, wrap='word')
text_widget.pack(expand=1, fill='both')

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

root.mainloop()
