import tkinter as tk
import tkinter as ttk
from tkinter import ttk, messagebox
from tkinter import font
from Util.Utils import *


class LogWindow:
    def __init__(self):
        self.log_window = None
        self.log_text = None
        self.current_font_size = 10  # 기본 폰트 크기
        self.text_font = None
        self.last_search_pos = "1.0"  # 마지막 검색 위치
        self.keyevent_window = None   # mutual 참조룰 위함
        self.log_instance = None
        self.find_dialog = None
        # 이벤트 수신자 등록

    def set_keyevent_window (self, window):
        self.keyevent_window = window

    def set_log_instance (self, log):
        self.log_instance = log

    def layout_LogWindow(self, root, dimension):

        self.log_window = tk.Toplevel(root)
        self.log_window.title("Log")
        self.log_window.geometry(dimension)

        # 닫기 버튼 비활성화
        self.log_window.protocol("WM_DELETE_WINDOW", self.disable_close_button)

        # 메뉴 추가
        self.create_menu()

        # 프레임
        frame = tk.Frame(self.log_window)
        frame.pack(expand=True, fill='both')

         # 텍스트 위젯  wrap='none' 은 line 이 긴 경우에 다음줄로 넘기지 않는다
        self.log_text = tk.Text(frame, wrap='none')
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # 기본 폰트 설정
        self.text_font = font.Font(family="Helvetica", size=self.current_font_size)
        self.log_text.configure(font=self.text_font)

        # 수직 스크롤 막대
        vscroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lambda *args: self.on_vertical_scroll(*args) or self.log_text.yview(*args))
        vscroll.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=vscroll.set)

        # 수평 스크롤 막대
        hscroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.log_text.xview)
        hscroll.grid(row=1, column=0, sticky="ew")
        self.log_text.config(xscrollcommand=hscroll.set)

        # 프레임 크기 조정
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

         # 마우스 휠 이벤트 바인딩
        self.log_text.bind("<Control-MouseWheel>", self.on_mouse_wheel)


    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.current_font_size += 1  # 폰트 크기 증가
        else:
            self.current_font_size -= 1  # 폰트 크기 감소
        self.text_font.configure(size=self.current_font_size)
        self.log_text.configure(font=self.text_font)


    def scroll_to_line(self, line_number):
        # Clear previous highlights
        self.log_text.tag_remove("highlight", "1.0", "end")

        # Scroll to the specified line number
        self.log_text.see(f"{line_number}.0")

        # Highlight the specified line
        self.log_text.tag_add("highlight", f"{line_number}.0", f"{line_number}.0 lineend")
        self.log_text.tag_configure("highlight", background="yellow")


    def on_vertical_scroll(self, *args):
        self.log_text.yview(*args)


    def create_menu(self):
        menubar = tk.Menu(self.log_window)

        # 편집 메뉴
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Find", command=lambda: self.create_find_dialog(self.log_window))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.log_window.config(menu=menubar)


    def find_next(self, search_text):

        print("JInha find_next", search_text)
        # 찾기 기능 구현
        start_pos = self.log_text.search(search_text, self.last_search_pos, tk.END)
        if not start_pos:
            print("Text not found")
            return

        end_pos = f"{start_pos}+{len(search_text)}c"

        # Clear previous highlights
        self.log_text.tag_remove("highlight", "1.0", tk.END)

        # 찾은 텍스트 강조
        self.log_text.tag_add("highlight", start_pos, end_pos)
        self.log_text.tag_configure("highlight", background="yellow")

        # 찾은 텍스트로 스크롤
        self.log_text.see(start_pos)

        # start_pos와 end_pos가 있는 라인의 텍스트 전체 얻기
        line_start = self.log_text.index(start_pos).split('.')[0]
        line_end = self.log_text.index(end_pos).split('.')[0]

    # 시작 라인부터 끝 라인까지의 모든 텍스트 얻기
        found_text = ""
        for line_num in range(int(line_start), int(line_end) + 1):
            line_text = self.log_text.get(f"{line_num}.0", f"{line_num}.end")
            found_text += line_text

        timestamp_str = extract_timestampstring(found_text)
        line_index = self.log_instance.locate_keyevent(timestamp_str)
        if line_index is not None:  # line_index가 None이 아닌지 확인
            self.keyevent_window.scroll_to_line(line_index)
        else:
            print ("line_index not valid")
        # 마지막 검색 위치 업데이트
        self.last_search_pos = end_pos


    def find_previous(self, search_text):
        # 역방향 찾기 기능 구현
        start_pos = self.log_text.search(search_text, self.last_search_pos, "1.0", backwards=True)
        if not start_pos:
            print("Text not found")
            return

        end_pos = f"{start_pos}+{len(search_text)}c"

        # 이전 강조 제거
        self.log_text.tag_remove("highlight", "1.0", tk.END)

        # 찾은 텍스트 강조
        self.log_text.tag_add("highlight", start_pos, end_pos)
        self.log_text.tag_configure("highlight", background="yellow")

        # 찾은 텍스트로 스크롤
        self.log_text.see(start_pos)

        # start_pos와 end_pos가 있는 라인의 텍스트 전체 얻기
        line_start = self.log_text.index(start_pos).split('.')[0]
        line_end = self.log_text.index(end_pos).split('.')[0]

    # 시작 라인부터 끝 라인까지의 모든 텍스트 얻기
        found_text = ""
        for line_num in range(int(line_start), int(line_end) + 1):
            line_text = self.log_text.get(f"{line_num}.0", f"{line_num}.end")
            found_text += line_text

        timestamp_str = extract_timestampstring(found_text)
        line_index = self.log_instance.locate_keyevent(timestamp_str)
        if line_index is not None:  # line_index가 None이 아닌지 확인
            self.keyevent_window.scroll_to_line(line_index)
        else:
            print ("line_index not valid")

        # 마지막 검색 위치 업데이트
        self.last_search_pos = start_pos


    def create_find_dialog(self, parent):

        # log_text에 내용이 있는지 확인
        if not self.log_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "Log content is empty. Cannot open Find dialog.")
            return

        if self.find_dialog is not None and self.find_dialog.winfo_exists():
            self.find_dialog.focus()
            return

        # Create a new top-level window
        self.find_dialog = tk.Toplevel(parent)
        self.find_dialog.withdraw()
        self.find_dialog.title("Find in Log")

        # Make the window resizable
        self.find_dialog.resizable(False, False)

        # Add a label and an entry widget
        label = ttk.Label(self.find_dialog, text="Find:")
        label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        search_entry = ttk.Entry(self.find_dialog)
        search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Enter 키 이벤트와 find_next 메서드를 연결합니다.
        search_entry.bind('<Return>', lambda event: self.find_next(search_entry.get()))
        
        # Add the buttons
        find_prev_button = ttk.Button(self.find_dialog, text="Find Prev", command=lambda: self.find_previous(search_entry.get()))
        find_prev_button.grid(row=1, column=0, padx=10, pady=10)

        find_next_button = ttk.Button(self.find_dialog, text="Find Next", command=lambda: self.find_next(search_entry.get()))
        find_next_button.grid(row=1, column=1, padx=10, pady=10)

        # Configure the grid to expand the entry widget
        self.find_dialog.grid_columnconfigure(1, weight=1)

        # Bind the Escape key to close the dialog
        self.find_dialog.bind('<Escape>', lambda event: self.find_dialog.destroy())

        # position the dialog on the screen
        self.find_dialog.update_idletasks()

        parent.update_idletasks()  # Ensure the parent window size and position are updated

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()

        dialog_width = self.find_dialog.winfo_width()
        dialog_height = self.find_dialog.winfo_height()

        x = parent_x + parent_width - dialog_width
        y = parent_y

        self.find_dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

        # 위치 설정 후 대화상자를 보이도록 설정
        self.find_dialog.deiconify()

        # Return the dialog to the main loop
        self.find_dialog.transient(parent)
        # self.find_dialog.grab_set()   # make it modal
        parent.wait_window(self.find_dialog)


    def disable_close_button(self):
        pass  # 아무 동작도 하지 않음