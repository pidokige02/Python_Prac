import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile

def read_zip_file(zip_path, file_to_read):

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if file_to_read in zip_ref.namelist():
                with zip_ref.open(file_to_read) as file:
                    content = file.read().decode('utf-8')  # 파일 내용을 문자열로 디코딩
                    return content
            else:
                return f"{file_to_read} not found in the ZIP archive"
    except zipfile.BadZipFile:
        return "Error: The file is not a valid ZIP file"

def open_zip_dialog():
    root = tk.Tk()
    root.withdraw()  # 기본 tkinter 윈도우 숨기기

    zip_path = filedialog.askopenfilename(title="Select ZIP file", filetypes=[("ZIP files", "*.zip")])

    if not zip_path:
        messagebox.showinfo("No file selected", "No file was selected. Please select a ZIP file.")
        return

    # 예시로 ZIP 파일 내의 특정 파일명을 하드코딩
    file_to_read = 'Devices_1.txt'
    print("Jinha", file_to_read, zip_path)
    content = read_zip_file(zip_path, file_to_read)

    if content:
        result_window = tk.Toplevel()
        result_window.title("File Content")

        text_area = tk.Text(result_window, wrap='word')
        text_area.insert(tk.END, content)
        text_area.pack(expand=True, fill='both')

        scroll_bar = tk.Scrollbar(result_window, command=text_area.yview)
        text_area.configure(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        messagebox.showinfo("Read Error", "Could not read the content from the ZIP file.")

    root.deiconify()  # Tkinter 윈도우를 다시 보이도록 설정
    root.mainloop()  # Tkinter 이벤트 루프 시작
# ZIP 파일 열기 대화상자를 실행
open_zip_dialog()
