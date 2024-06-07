import tkinter as tk
from tkinter import font

class LogWindow:
    def __init__(self):
        self.log_window = None
        self.log_text = None 
        self.current_font_size = 10  # 기본 폰트 크기
        self.text_font = None        

    def layout_LogWindow(self, root, dimension):

        self.log_window = tk.Toplevel(root)
        self.log_window.title("Log")
        self.log_window.geometry(dimension)

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