from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication
from first_window import MainWindow
from touchIdWindow import ddUi_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(self.width, self.height)  # Set fixed size
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set background color to white
        self.centralwidget.setStyleSheet("background-color: white;")

        self.faceIDbutton = None  # Define as None initially
        self.touchIDbutton = None
        self.registration = None

        main_window_width = MainWindow.frameGeometry().width()
        button_width = 200  # Button width as set in createButtonWithLabel
        x_coordinate = int(self.width * 0.3)

        self.createButtonWithLabel(x_coordinate, int(self.height * 0.35), "Face ID", "faceIDbutton")
        self.createButtonWithLabel(x_coordinate, int(self.height * 0.55) , "Touch ID", "touchIDbutton")
        # self.createButtonWithLabel(x_coordinate, 70 + 2 * (150 + 91), "Регистрация", "registration")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    # Rest of the code remains the same

    def createButtonWithLabel(self, x, y, label_text, button_object):
        button = QtWidgets.QPushButton(self.centralwidget)
        button.setGeometry(QtCore.QRect(x, y, int(self.width * 0.4), int(self.height * 0.1)))
        button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/button1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(int(self.width * 0.4), int(self.height * 0.8)))
        button.setFlat(True)
        button.setObjectName(button_object)

        label_width = int(self.width * 0.4)  # Adjust according to your preference
        label_height = int(self.width * 0.05)  # Adjust according to your preference
        label_x = int((button.width() - label_width) / 2)
        label_y = int((button.height() - label_height) / 2)

        label = QtWidgets.QLabel(button)
        label.setGeometry(QtCore.QRect(label_x, label_y, label_width, label_height))
        label.setText(label_text)
        button.setStyleSheet("background-color: transparent; color: white; border: none;")  # Set button styles
        font = label.font()
        font.setPixelSize(int(label_width / 15))
        label.setFont(font)
        label.setStyleSheet("color: white;")
        label.setAlignment(QtCore.Qt.AlignCenter)

        if button_object == "faceIDbutton":
            self.faceIDbutton = button
        elif button_object == "touchIDbutton":
            self.touchIDbutton = button

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # No changes needed here since the label text is set in code

class dMyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showFullScreen()
        self.touchIDw = None
        self.current_recording = None
        self.ui.faceIDbutton.clicked.connect(self.first_checkup_clicked)
        self.ui.touchIDbutton.clicked.connect(self.second_checkup_clicked)

    def open_first_window(self):
        self.first_window = MainWindow()
        self.first_window.showFullScreen()
        self.close()  # Close the current window
        self.close()  # Close the current window

    def opemTouchIDwindow(self):
        self.touchIDw = QMainWindow()
        self.ui = ddUi_MainWindow()
        self.ui.setupUi(self.touchIDw)
        self.touchIDw.showFullScreen()
        self.close()  # Close the current window
     # Close the current window


    def first_checkup_clicked(self):
        self.open_first_window()

    def second_checkup_clicked(self):
        self.opemTouchIDwindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = dMyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())