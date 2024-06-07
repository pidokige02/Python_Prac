import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Example")
        self.root.geometry("600x400")

        # Treeview 생성
        self.tree = ttk.Treeview(root, columns=("col1", "col2", "col3"), show='headings')
        
        # 각 열의 제목 설정
        self.tree.heading("col1", text="Column 1")
        self.tree.heading("col2", text="Column 2")
        self.tree.heading("col3", text="Column 3")

        # 열 너비 설정
        self.tree.column("col1", width=150)
        self.tree.column("col2", width=150)
        self.tree.column("col3", width=150)

        # 데이터 삽입
        data = [
            ("Row 1, Column 1", "Row 1, Column 2", "Row 1, Column 3"),
            ("Row 2, Column 1", "Row 2, Column 2", "Row 2, Column 3"),
            ("Row 3, Column 1", "Row 3, Column 2", "Row 3, Column 3"),
        ]

        for item in data:
            self.tree.insert("", tk.END, values=item)

        # Treeview 패킹
        self.tree.pack(expand=True, fill=tk.BOTH)

        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # TreeviewSelect 이벤트 바인딩
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event):
        # 선택된 항목들 가져오기
        selected_items = self.tree.selection()
        for item in selected_items:
            item_text = self.tree.item(item, "values")
            print(f"Selected item: {item_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()