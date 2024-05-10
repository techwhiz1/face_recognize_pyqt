from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication
from PyQt5.QtGui import QImage, QPixmap
from globalval  import global_health_check

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from camera import CameraWindow  # Importing CameraWindow from the camera module
import re
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.width * 0.3), int(self.height * 0.2), int(self.width * 0.4), int(self.height * 0.1)))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(int(self.width * 0.3), int(self.height * 0.3), int(self.width * 0.4), int(self.height * 0.1)))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.setupLabelPalette()

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(int(self.width * 0.3), int(self.height * 0.6), int(self.width * 0.4), int(self.height * 0.1)))
        self.setupButtonStyle()

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(int(self.width * 0.3), int(self.height * 0.4), int(self.width * 0.4), int(self.height * 0.1)))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.lineEdit.setFont(font)
        self.lineEdit.setInputMethodHints(
            QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhFormattedNumbersOnly | QtCore.Qt.ImhNoPredictiveText | QtCore.Qt.ImhPreferNumbers)

        # Setting the RegExpValidator for the lineEdit to accept exactly 12 digits
        reg_ex = QRegExp("^[0-9]{12}$")
        input_validator = QRegExpValidator(reg_ex, self.lineEdit)
        self.lineEdit.setValidator(input_validator)

        self.lineEdit.setMaxLength(12)  # Ensure the max length is 12
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.first_input = None
        self.pushButton_3.clicked.connect(self.handle_button_click)

    def setupLabelPalette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(122, 107, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(35)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

    def setupButtonStyle(self):
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                background-color: #8574f2;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                text-align: center;
                border: none;
            }
            QPushButton:hover {
                background-color: #9b8fee;
            }
            QPushButton:pressed {
                background-color: #7662e4;
            }
        """)
        self.pushButton_3.setObjectName("pushButton_3")

    def setupLineEditStyle(self):
        font = QtGui.QFont()
        font.setPointSize(40)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Registration"))
        self.label_2.setText(_translate("MainWindow", "Введите ИИН"))
        self.pushButton_3.setText(_translate("MainWindow", "Подтвердить"))

    def handle_button_click(self):
        text = self.lineEdit.text()
        if not re.fullmatch(r"\d{12}", text):
            _translate = QtCore.QCoreApplication.translate
            self.label_2.setText(_translate("MainWindow", "Подтвердите ИИН"))
            self.lineEdit.clear()
            return

        if self.first_input is None:
            self.first_input = text
            _translate = QtCore.QCoreApplication.translate
            self.label_2.setText(_translate("MainWindow", "Подтвердите ИИН"))
        else:
            if self.first_input == text:
                _translate = QtCore.QCoreApplication.translate
                self.label_2.setText(_translate("MainWindow", "Отлично"))

                global_health_check.addID(self.first_input)


                self.open_camera_window(self.first_input)
                self.closemain_window()

                # Save the first_input to the dictionary



            else:
                _translate = QtCore.QCoreApplication.translate
                self.label_2.setText(_translate("MainWindow", "Неправильно!"))
            self.first_input = None  # Reset for the next comparison

        self.lineEdit.clear()

    def open_camera_window(self, input_id):


        self.cam_window = CameraWindow(input_id)
        self.cam_window.showFullScreen()

    def closemain_window(self):
        if self.mainwindow:
            self.mainwindow.close()




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
