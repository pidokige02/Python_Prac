import tkinter as tk
from tkinter import ttk, messagebox
import re

class KeylogPlayer:
    def __init__(self, root):
        self.root = root
        self.command = None

    def show_input_dialog(self, default_command=""):
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter values")

        # 창 크기 조절 비활성화
        dialog.resizable(True, False)

        # Set dialog size and make it modal
        dialog.geometry("320x100")
        dialog.grab_set()

        def on_ok():
            command = command_entry.get()
            self.command = command
            dialog.destroy()


        def on_cancel():
            self.command = None
            dialog.destroy()

        # Configure the grid to make the entry expand
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

        # Command label and entry
        command_label = ttk.Label(dialog, text="Command")
        command_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=10, sticky='w')

        command_entry = ttk.Entry(dialog, width=50)  # 너비 설정
        command_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10, sticky='ew')
        command_entry.insert(0, default_command)  # 기본값 설정

        # OK and Cancel buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
        ok_button.pack(side="left", padx=(0, 5))

        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side="left", padx=(5, 0))

        self.root.wait_window(dialog)
        return self.command


    # def is_valid_ip(self, ip):
    #     ip = ip.strip()  # 앞뒤 공백 제거
    #     pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    #     match = pattern.match(ip)
    #     if match:
    #         for num in ip.split('.'):
    #             if not (0 <= int(num) <= 255):
    #                 print(f"범위 초과: {num}")
    #                 return False
    #         return True
    #     else:
    #         print("정규 표현식 일치 실패")
    #     return False