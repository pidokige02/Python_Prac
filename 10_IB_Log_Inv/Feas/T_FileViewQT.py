from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog
import sys

class FileViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.open_button = QPushButton('Open File', self)
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        self.setLayout(self.layout)
        self.setWindowTitle('File Viewer')

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setText(content)

app = QApplication(sys.argv)
viewer = FileViewer()
viewer.show()
sys.exit(app.exec_())
