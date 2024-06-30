import tkinter as tk

class CustomEventExample:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Event Example")

        # 1. 사용자 정의 이벤트 문자열 정의
        self.CUSTOM_EVENT = "<<CustomEvent>>"

        # 2. 이벤트 생성 및 발생
        self.create_widgets()
        self.trigger_custom_event()

    def create_widgets(self):
        button = tk.Button(self.root, text="Fire Custom Event", command=self.trigger_custom_event)
        button.pack(padx=20, pady=20)

        # 3. 이벤트 핸들링
        self.root.bind(self.CUSTOM_EVENT, lambda event, data="Custom": self.custom_event_handler(event, data))


    def trigger_custom_event(self):
        print("Custom event fired!")
        self.root.event_generate(self.CUSTOM_EVENT, data="Custom data1111")

    def custom_event_handler(self, event, data):
        print(f"Custom event data: {data}")

    def run(self):
        self.root.mainloop()

# 프로그램 실행
if __name__ == "__main__":
    app = CustomEventExample()
    app.run()
