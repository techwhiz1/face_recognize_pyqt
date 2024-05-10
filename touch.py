from PyQt5 import QtCore, QtGui, QtWidgets
from globalval import global_health_check
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


import sys
import subprocess
import os
import serial
import time
from reque import HealthCheck  # Make sure this path is correct
import threading
import second_window


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.mainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(228, 231, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(228, 231, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(228, 231, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(228, 231, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(600, 100, 1171, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(122, 107, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(122, 107, 223))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(35)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(840, 400, 240, 320))
        self.frame.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: black; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 20, 200, 280))
        self.frame_2.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: rgb(106, 255, 60); /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.start_serial_thread()
        
        self.closemain_window()
        self.open_second_window()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Подождите, идет загузка"))

    def start_serial_thread(self):
        self.thread = threading.Thread(target=self.serial_communication)
        self.thread.start()



    def serial_communication(self):
        with serial.Serial('COM4', 9600, timeout=1) as ser:
            print(f"Connected to fingerprint sensor on {ser.name}")
            try:
                time.sleep(2)
                command= 'ENROLL'
                print(f"Enrollol")
                ser.write(f"{command}\r\n".encode())
                time.sleep(2)
                last_id = global_health_check.getLastRecordedIDKey()
                lastid=str(last_id)
                ser.write(f"{lastid}\r\n".encode())
                print("Last ID sent:", lastid)
                time.sleep(1)
                while True:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        print(line)  # Print whatever message is received from the sensor
                        if line.lower() =="put":
                            self.update_label("Поставьте палец на датчик")
                        elif line.lower() == "remove":
                            self.update_label("Уберите палец")
                        elif line.lower() == "putsame":
                            self.update_label("Поставьте тот же палец на датчик")
                        elif line.lower() =="stored":
                            self.update_label("Отпечаток сохранен")
                            time.sleep(2)
                            ser.close()
                            print("COM5 closed")
                            self.closemain_window()
                            self.open_second_window()
                            break
            except Exception as e:
                print("Error with serial communication:", e)
            finally:
                ser.close()
                print("COM4 closed")

    def update_label(self, text):
        # Function to safely update label from the main thread
        def func():
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("MainWindow", text))

        QtCore.QMetaObject.invokeMethod(self.label, 'setText', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, text))

    def open_second_window(self):
        app = QApplication(sys.argv)
        self.smainWindow = second_window.MyMainWindow()
        self.smainWindow.showFullScreen()

        sys.exit(app.exec_())

    def closemain_window(self):
        if self.mainWindow:
            self.mainWindow.close()







