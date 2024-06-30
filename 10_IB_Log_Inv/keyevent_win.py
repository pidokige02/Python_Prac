import tkinter as tk
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

    def set_log_window(self, window):
        self.log_window = window

    def layout_KeyEventWindow(self, root, dimension):

        self.keyevent_window = tk.Toplevel(root)
        self.keyevent_window.title("Key Log")
        self.keyevent_window.geometry(dimension)

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


    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.current_font_size += 1  # 폰트 크기 증가
        else:
            self.current_font_size -= 1  # 폰트 크기 감소
        self.text_font.configure(size=self.current_font_size)
        self.keyevent_text.configure(font=self.text_font)


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
        edit_menu.add_command(label="Find", command=self.find)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.keyevent_window.config(menu=menubar)

    def find(self):
        if self.find_dialog is not None and self.find_dialog.winfo_exists():
            self.find_dialog.focus()
            return

        # 찾기 대화 상자를 생성하는 코드
        find_dialog = tk.Toplevel(self.keyevent_window)
        find_dialog.title("Find in KeyLog")

        tk.Label(find_dialog, text="Find:").grid(row=0, column=0, padx=4, pady=4)

        search_entry = tk.Entry(find_dialog)
        search_entry.grid(row=0, column=1, padx=4, pady=4)

        tk.Button(find_dialog, text="Find Prev", command=lambda: self.find_previous(search_entry.get())).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(find_dialog, text="Find Next", command=lambda: self.find_next(search_entry.get())).grid(row=1, column=1, padx=2, pady=2)


    def find_next(self, search_text):
        # 찾기 기능 구현
        start_pos = self.keyevent_text.search(search_text, self.last_search_pos, tk.END)
        if not start_pos:
            print("Text not found")
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

        self.log_window.scroll_to_line(200)


    def find_previous(self, search_text):
        # 역방향 찾기 기능 구현
        start_pos = self.keyevent_text.search(search_text, self.last_search_pos, "1.0", backwards=True)
        if not start_pos:
            print("Text not found")
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

        self.log_window.scroll_to_line(100)
