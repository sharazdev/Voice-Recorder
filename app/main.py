import sys
from PyQt5.QtWidgets import QApplication
from model import AudioRecorder
from view import MainWindow
from controller import Controller

def main():
    app = QApplication(sys.argv)
    model = AudioRecorder()
    view = MainWindow()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()