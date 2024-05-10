# main.py
import sys
from PyQt5.QtWidgets import QApplication
from second_window import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
