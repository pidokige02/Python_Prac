import tkinter as tk
from tkinter import ttk
from configure_data import *

#pane 에 peripheral만 표시하는 window 임 
class PeripheralWindow:
    def __init__(self):
        self.pane1 = None
        self.tree = None 


    def layout_PeripheralWindow(self, root):
        # root 에는 notebook 이 실랴오고, 
        self.pane1 = ttk.Frame(root) # root 를 parent 로 panel 을 만들음.
        root.add(self.pane1, text='Peripherals')  # panel 을 notebook 에 추가함

        # Treeview 생성
        self.tree = ttk.Treeview(self.pane1, columns=treeview_index, show='headings')  # panel 을 parent 로 하여 TreeView 를 만든다.

        for col_name, col_text, col_width in peripheral_columns:
            self.tree.heading(col_name, text=col_text) # 각 열의 제목 설정
            self.tree.column(col_name, width=col_width)  # 열의 너비를 설정 (옵션)

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.pane1, orient="vertical", command=self.tree.yview) # scroll bar 도 panel 을 parent 로 만든다.
        self.tree.configure(yscroll=scrollbar.set)

        # Treeview와 스크롤바를 grid로 배치
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # grid 레이아웃을 사용하여 크기 조정
        self.pane1.grid_rowconfigure(0, weight=1)
        self.pane1.grid_columnconfigure(0, weight=1)
        
            # TreeviewSelect 이벤트 바인딩
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)


    def update_PeripheralWindow (self, filtered_df):

        # 기존 데이터를 모두 제거
        for item in self.tree.get_children():
            self.tree.delete(item)

        # DataFrame의 각 행을 Treeview에 삽입
        for index, row in filtered_df.iterrows():
            self.tree.insert("", tk.END, values=(row['Name'], row['ProductName'], row['MfgName'], row['Status']))


    def on_tree_select(self, event):
        # 선택된 항목들 가져오기
        selected_items = self.tree.selection()
        for item in selected_items:
            item_text = self.tree.item(item, "values")
            print(f"Selected item: {item_text}")
