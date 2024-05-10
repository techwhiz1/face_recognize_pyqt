from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow  # Import QApplication and QMainWindow
import cv2
import os
from globalval  import global_health_check
from touch import Ui_MainWindow as ssUi_MainWindow
import time

class CameraWindow(QtWidgets.QMainWindow):
    def __init__(self, input_id):
        super().__init__()

        self.input_id  = global_health_check.getLastRecordedID()

        self.Touchreg = None
        self.camera = cv2.VideoCapture(0)  # Adjust camera index if necessary
        if not self.camera.isOpened():
            print("Error: Camera could not be opened")
            return

        # Set the resolution to 1080p

        print("Camera initialized: ", self.camera.isOpened())
        self.initUI()

    def initUI(self):
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        start = time.time()
        # Create a QLabel to display the camera feed
        self.camera_label = QtWidgets.QLabel(self)
        self.camera_label.setGeometry(QtCore.QRect(int(self.width * 0.3), int(self.height * 0.2), int(self.width * 0.4), int(self.height * 0.5)))
        # Ensure the label is scaled to its contents
        self.camera_label.setScaledContents(True)

        # Start capturing the camera feed
        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

        # Create a QPushButton to take a picture
        self.take_pic_btn = QtWidgets.QPushButton("Сделать фото", self)
        self.take_pic_btn.setGeometry(int(self.width * 0.325), int(self.height * 0.75), int(self.width * 0.35), int(self.height * 0.1))
        self.styleButton(self.take_pic_btn)
        self.take_pic_btn.clicked.connect(self.take_picture)
        print("time: ", time.time() - start)

    def update_frame(self):
        start = time.time()
        ret, frame = self.camera.read()

        if not ret:
            print("Failed to grab frame")
            return

        # Convert the frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to a QImage
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        # Convert the QImage to a QPixmap and set it to the camera label
        pixmap = QPixmap.fromImage(image)
        self.camera_label.setPixmap(pixmap)
        print("update_frame_time: ", time.time() - start)

    def take_picture(self):
        ret, frame = self.camera.read()
        if ret:
            if not os.path.exists('faces'):
                os.makedirs('faces')
            filename = f"faces/{self.input_id}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")

            self.touchRegWindow = QMainWindow()
            self.ui = ssUi_MainWindow()
            self.ui.setupUi(self.touchRegWindow)
            self.touchRegWindow.showFullScreen()

            # Open the touch window from touch.py
            self.close()



        else:
            print("Error taking picture")
        self.timer.stop()  # Stop the timer
        self.camera.release()  # Release the camera


    def styleButton(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #8574f2;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 25px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #9b8fee;
            }
            QPushButton:pressed {
                background-color: #7662e4;
            }
        """)
