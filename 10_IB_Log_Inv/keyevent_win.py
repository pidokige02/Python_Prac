import tkinter as tk

# keyboard 의 history 를 보여주는 window.
class KeyEventWindow:
    def __init__(self):
        self.keyevent_window = None
        self.log_text = None 


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

