import tkinter as tk
import tkinter as ttk
from tkinter import ttk, messagebox
from tkinter import font

# keyboard 의 history 를 보여주는 window.
class KeyEventWindow:
    def __init__(self):
        self.keyevent_window = None
        self.keyevent_text = None
        self.current_font_size = 10  # 기본 폰트 크기
        self.text_font = None
        self.last_search_pos = "1.0"  # 마지막 검색 위치
        self.log_window = None
        self.find_dialog = None
        self.last_opened_keyevent_files = []
        
    def set_log_window(self, window):
        self.log_window = window

    def resize_KeyEventWindow(self, dimension):
        self.keyevent_window.geometry(dimension)


    def layout_KeyEventWindow(self, root, dimension):

        self.keyevent_window = tk.Toplevel(root)
        self.keyevent_window.title("Key Log")
        self.keyevent_window.geometry(dimension)

        # 닫기 버튼 비활성화
        self.keyevent_window.protocol("WM_DELETE_WINDOW", self.disable_close_button)

        # 메뉴 추가
        self.create_menu()

        # 프레임
        frame_keyevent = tk.Frame(self.keyevent_window)
        frame_keyevent.pack(expand=True, fill='both')

        # 텍스트 위젯 wrap='none' 은 line 이 긴 경우에 다음줄로 넘기지 않는다
        self.keyevent_text = tk.Text(frame_keyevent, wrap='none')
        self.keyevent_text.grid(row=0, column=0, sticky="nsew")

        # 기본 폰트 설정
        self.text_font = font.Font(family="Helvetica", size=self.current_font_size)
        self.keyevent_text.configure(font=self.text_font)

        # 수직 스크롤 막대
        vscroll_key = tk.Scrollbar(frame_keyevent, orient=tk.VERTICAL, command=lambda *args: self.on_vertical_scroll(*args) or self.keyevent_text.yview(*args))
        vscroll_key.grid(row=0, column=1, sticky="ns")
        self.keyevent_text.config(yscrollcommand=vscroll_key.set)

        # 수평 스크롤 막대
        hscroll_key = tk.Scrollbar(frame_keyevent, orient=tk.HORIZONTAL, command=self.keyevent_text.xview)
        hscroll_key.grid(row=1, column=0, sticky="ew")
        self.keyevent_text.config(xscrollcommand=hscroll_key.set)

        # 프레임 크기 조정
        frame_keyevent.grid_rowconfigure(0, weight=1)
        frame_keyevent.grid_columnconfigure(0, weight=1)

         # 마우스 휠 이벤트 바인딩
        self.keyevent_text.bind("<Control-MouseWheel>", self.on_mouse_wheel)
        # 화살표 키 이벤트 바인딩
        self.keyevent_text.bind("<Up>", self.scroll_up)
        self.keyevent_text.bind("<Down>", self.scroll_down)

        # 페이지 업/다운 키 이벤트 바인딩
        self.keyevent_text.bind("<Prior>", self.page_up)
        self.keyevent_text.bind("<Next>", self.page_down)



    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.current_font_size += 1  # 폰트 크기 증가
        else:
            self.current_font_size -= 1  # 폰트 크기 감소
        self.text_font.configure(size=self.current_font_size)
        self.keyevent_text.configure(font=self.text_font)


    def scroll_up(self, event):
        self.keyevent_text.yview_scroll(-1, "units")

    def scroll_down(self, event):
        self.keyevent_text.yview_scroll(1, "units")

    def page_up(self, event):
        self.keyevent_text.yview_scroll(-1, "pages")

    def page_down(self, event):
        self.keyevent_text.yview_scroll(1, "pages")
        
    def scroll_to_line(self, line_number):
        # Clear previous highlights
        self.keyevent_text.tag_remove("highlight", "1.0", "end")

        # Scroll to the specified line number
        self.keyevent_text.see(f"{line_number}.0")

        # Highlight the specified line
        self.keyevent_text.tag_add("highlight", f"{line_number}.0", f"{line_number}.0 lineend")
        self.keyevent_text.tag_configure("highlight", background="yellow")

    def on_vertical_scroll(self, *args):
        self.keyevent_text.yview(*args)


    def create_menu(self):
        menubar = tk.Menu(self.keyevent_window)

        # 편집 메뉴
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Find", command=lambda: self.create_find_dialog(self.keyevent_window))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.keyevent_window.config(menu=menubar)


    def find_next_from_entry(self, search_entry):
        search_text = search_entry.get()
        self.find_next(search_text)

    def find_previous_from_entry(self, search_entry):
        search_text = search_entry.get()
        self.find_previous(search_text)


    def find_next(self, search_text):
        # 찾기 기능 구현
        print("find_next", search_text, self.last_search_pos)
        start_pos = self.keyevent_text.search(search_text, self.last_search_pos, tk.END)
        if not start_pos:
            print("Text not found")
            self.last_search_pos = "1.0"  # initialize last_search_pos.
            return

        end_pos = f"{start_pos}+{len(search_text)}c"

        # Clear previous highlights
        self.keyevent_text.tag_remove("highlight", "1.0", tk.END)

        # Highlight the found text
        self.keyevent_text.tag_add("highlight", start_pos, end_pos)
        self.keyevent_text.tag_configure("highlight", background="yellow")

        # 찾은 텍스트로 스크롤
        self.keyevent_text.see(start_pos)

        # 마지막 검색 위치 업데이트
        self.last_search_pos = end_pos


    def find_previous(self, search_text):
        # 역방향 찾기 기능 구현
        start_pos = self.keyevent_text.search(search_text, self.last_search_pos, "1.0", backwards=True)
        if not start_pos:
            print("Text not found")
            self.last_search_pos = "1.0"  # initialize last_search_pos.
            return

        end_pos = f"{start_pos}+{len(search_text)}c"

        # 이전 강조 제거
        self.keyevent_text.tag_remove("highlight", "1.0", tk.END)

        # 찾은 텍스트 강조
        self.keyevent_text.tag_add("highlight", start_pos, end_pos)
        self.keyevent_text.tag_configure("highlight", background="yellow")

        # 찾은 텍스트로 스크롤
        self.keyevent_text.see(start_pos)

        # 마지막 검색 위치 업데이트
        self.last_search_pos = start_pos


    def create_find_dialog(self, parent):

        # log_text에 내용이 있는지 확인
        if not self.keyevent_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "Log content is empty. Cannot open Find dialog.")
            return

        if self.find_dialog is not None and self.find_dialog.winfo_exists():
            self.find_dialog.focus()
            return
        
        self.last_search_pos = "1.0"  # initialize last_search_pos.  
        # Create a new top-level window
        self.find_dialog = tk.Toplevel(parent)
        self.find_dialog.withdraw()
        self.find_dialog.title("Find in KeyLog")

        # Make the window resizable
        self.find_dialog.resizable(False, False)

        # Add a label and an entry widget
        label = ttk.Label(self.find_dialog, text="Find:")
        label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        search_entry = ttk.Entry(self.find_dialog)
        search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Enter 키 이벤트와 find_next 메서드를 연결합니다.
        search_entry.bind('<Return>', lambda event: self.find_next_from_entry(search_entry))
        
        # Add the buttons
        find_prev_button = ttk.Button(self.find_dialog, text="Find Prev", command=lambda: self.find_previous_from_entry(search_entry))
        find_prev_button.grid(row=1, column=0, padx=10, pady=10)

        find_next_button = ttk.Button(self.find_dialog, text="Find Next", command=lambda: self.find_next_from_entry(search_entry))
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

        dialog_width = self.find_dialog.winfo_width()
        dialog_height = self.find_dialog.winfo_height()

        x = parent_x - dialog_width  #  position find dialog on the right side of parent window 
        y = parent_y  #  

        self.find_dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

        # 위치 설정 후 대화상자를 보이도록 설정
        self.find_dialog.deiconify()

        # Return the dialog to the main loop
        self.find_dialog.transient(parent)
        # self.find_dialog.grab_set()   # make it modess
        parent.wait_window(self.find_dialog)


    def disable_close_button(self):
        pass  # 아무 동작도 하지 않음


    def get_matching_lines(self, search_text):
        start_pos = "1.0"
        matching_lines = []

        while True:
            start_pos = self.keyevent_text.search(search_text, start_pos, tk.END)
            if not start_pos:
                break
            line_number = start_pos.split(".")[0]
            matching_lines.append(line_number)
            start_pos = f"{start_pos}+1c"

        return matching_lines 
    

    def clear_highlight(self):
        # Remove all highlights
        self.keyevent_text.tag_remove("highlight", "1.0", "end")
