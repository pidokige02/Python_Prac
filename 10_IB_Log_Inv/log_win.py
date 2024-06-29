import tkinter as tk
from tkinter import font

class LogWindow:
    def __init__(self):
        self.log_window = None
        self.log_text = None
        self.current_font_size = 10  # 기본 폰트 크기
        self.text_font = None
        self.last_search_pos = "1.0"  # 마지막 검색 위치

    def layout_LogWindow(self, root, dimension):

        self.log_window = tk.Toplevel(root)
        self.log_window.title("Log")
        self.log_window.geometry(dimension)

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
        edit_menu.add_command(label="Find", command=self.find)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.log_window.config(menu=menubar)

    def find(self):
        # 찾기 대화 상자를 생성하는 코드
        find_dialog = tk.Toplevel(self.log_window)
        find_dialog.title("Find")

        tk.Label(find_dialog, text="Find:").grid(row=0, column=0, padx=4, pady=4)

        search_entry = tk.Entry(find_dialog)
        search_entry.grid(row=0, column=1, padx=4, pady=4)

        tk.Button(find_dialog, text="Find Next", command=lambda: self.find_next(search_entry.get())).grid(row=1, column=0, columnspan=2, pady=4)

    def find_next(self, search_text):
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

        # 마지막 검색 위치 업데이트
        self.last_search_pos = end_pos
