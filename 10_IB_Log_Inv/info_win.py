import tkinter as tk
from tkinter import ttk
from configure_data import *


class InfoWindow:
    def __init__(self):
        self.pane1 = None
        self.text  = None 


    def layout_InfoWindow(self, root):
        self.pane1 = ttk.Frame(root)
        root.add(self.pane1, text='Info')

        # Text 위젯 생성
        self.text = tk.Text(self.pane1, wrap='word', state='disabled')  # Text 위젯을 disabled 상태로 생성

        # Text 위젯에 텍스트 삽입 (임시로 'normal' 상태로 변경하여 삽입)
        self.text.config(state='normal')
        self.text.insert('1.0', "This is Pane 2\n" * 20)
        self.text.config(state='disabled')

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.pane1, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        # Text 위젯과 스크롤바를 grid로 배치
        self.text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # grid 레이아웃을 사용하여 크기 조정
        self.pane1.grid_rowconfigure(0, weight=1)
        self.pane1.grid_columnconfigure(0, weight=1)        
   
