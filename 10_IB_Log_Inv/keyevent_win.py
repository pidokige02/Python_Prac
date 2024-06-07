import tkinter as tk
from tkinter import font

# keyboard 의 history 를 보여주는 window.
class KeyEventWindow:
    def __init__(self):
        self.keyevent_window = None
        self.log_text = None 
        self.current_font_size = 10  # 기본 폰트 크기
        self.text_font = None        


    def layout_KeyEventWindow(self, root, dimension):

        self.keyevent_window = tk.Toplevel(root)
        self.keyevent_window.title("Key Log")
        self.keyevent_window.geometry(dimension)


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


    def on_vertical_scroll(self, *args):
        self.keyevent_text.yview(*args)
    