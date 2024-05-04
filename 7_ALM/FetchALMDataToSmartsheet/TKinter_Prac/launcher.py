from tkinter import *

root = Tk()
root.title("SPR Automation")
root.geometry("640x240")
root.resizable(False, False)
# root.configure(background="cyan")



label1 = Label(root, text="SPR 을 얻어오고 싶은 project를  선택하고 실행 button을 누르세요.")
# label1.pack(side="left")   # center left 에 붙는다.
label1.pack(anchor="nw", padx=10, pady=10)   # top left에 붙는다 간경을 10 point 만큼 벌린다


def execute():
    print("선택된 check box %d, %d, %d" % (osprey_r4.get(), gemini_r4.get(), gemini_r5.get()) )



osprey_r4 = IntVar() # chkvar 에 int 형으로 값을 저장한다
osprey_r4_chkbox = Checkbutton(root, text="Osprey R4", variable=osprey_r4)
osprey_r4_chkbox.select() # 자동 선택 처리
# chkbox.deselect() # 선택 해제 처리
osprey_r4_chkbox.pack(anchor="nw", padx=10, pady=5)


gemini_r4 = IntVar()
gemini_r4_chkbox = Checkbutton(root, text="Gemini R4", variable=gemini_r4)
gemini_r4_chkbox.select() # 자동 선택 처리
gemini_r4_chkbox.pack(anchor="nw", padx=10, pady=5)

gemini_r5 = IntVar()
gemini_r5_chkbox = Checkbutton(root, text="Gemini R5", variable=gemini_r5)
gemini_r5_chkbox.select() # 자동 선택 처리
gemini_r5_chkbox.pack(anchor="nw", padx=10, pady=5)


btn = Button(root, text="실행", command=execute, width=20)
btn.pack(side="bottom", pady=30)

root.mainloop()