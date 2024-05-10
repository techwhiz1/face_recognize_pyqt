from PyQt5 import QtCore, QtGui, QtWidgets
from first_window import MainWindow
from datetime import datetime
from chooseType import dMyMainWindow
from globalval import global_health_check
from RegistrationWIndow import Ui_MainWindow as RegistrationUi
from first_window import VideoThread
from camera import CameraWindow  # Importing CameraWindow from the camera module
from PyQt5.QtWidgets import QApplication, QWidget

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

        self.first_checkup = None  # Define as None initially
        self.second_checkup = None
        self.registration = None

        main_window_width = MainWindow.frameGeometry().width()
        button_width = 1000  # Button width as set in createButtonWithLabel
        x_coordinate = int(self.width * 0.1)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.width * 0.1), int(self.height * 0.1), int(self.width * 0.8), int(self.height * 0.3)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(122, 107, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont('Helvetica [Cronyx]')
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(900)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Select scan type", "Выберите тип проверки"))

        self.createButtonWithLabel(x_coordinate, int(self.height * 0.4), "Предсменный/предрейсовый медицинский осмотр", "first_checkup")
        self.createButtonWithLabel(x_coordinate, int(self.height * 0.55), "Послесменный/послерейсовый медицинский осмотр", "second_checkup")
        self.createButtonWithLabel(x_coordinate, int(self.height * 0.7), "Регистрация", "registration")

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
        button.setGeometry(QtCore.QRect(x, y, int(self.width * 0.8), int(self.height * 0.13)))
        button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/button1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(int(self.width * 0.8), int(self.height * 0.8)))
        button.setFlat(True)
        button.setObjectName(button_object)

        label_width = int(self.width * 0.7)  # Adjust according to your preference
        label_height = int(self.width * 0.05)  # Adjust according to your preference
        label_x = int((button.width() - label_width) / 2)
        label_y = int((button.height() - label_height) / 2)

        label = QtWidgets.QLabel(button)
        label.setGeometry(QtCore.QRect(label_x, label_y, label_width, label_height))
        label.setText(label_text)
        button.setStyleSheet("background-color: transparent; color: white; border: none;")  # Set button styles
        
        font = label.font()
        font = QtGui.QFont('Times')
        font.setPixelSize(int(label_width / 30))
        label.setFont(font)
        label.setStyleSheet("color: white;")
        label.setAlignment(QtCore.Qt.AlignCenter)

        if button_object == "first_checkup":
            self.first_checkup = button
        elif button_object == "second_checkup":
            self.second_checkup = button
        elif button_object == "registration":
            self.registration = button

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # No changes needed here since the label text is set in code


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showFullScreen()
        self.current_recording = None  # Add this line
        self.ui.first_checkup.clicked.connect(self.first_checkup_clicked)
        self.ui.second_checkup.clicked.connect(self.second_checkup_clicked)
        self.ui.registration.clicked.connect(self.registration_clicked)  # Connect registration button click event

    def open_first_window(self):
        self.first_window = MainWindow()
        self.first_window.show()
        self.close()  # Close the current window

    def openChoice(self):
        self.choice_window = dMyMainWindow()
        self.choice_window.show()
        self.close()

    def first_checkup_clicked(self):
        self.openChoice()
        global_health_check.checkup = 1
        VideoThread.update_database_from_folder("faces", "data.pkl")

    def second_checkup_clicked(self):
        self.openChoice()
        global_health_check.checkup = 2
        VideoThread.update_database_from_folder("faces", "data.pkl")

    def registration_clicked(self):
        # Close the second window
        self.close()
        # Open the registration window
        self.open_registration_window()

    def open_registration_window(self):
        self.registration_window = QtWidgets.QMainWindow()
        self.registration_ui = RegistrationUi()
        self.registration_ui.setupUi(self.registration_window)
        self.registration_window.showMaximized()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
