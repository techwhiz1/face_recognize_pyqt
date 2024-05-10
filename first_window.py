import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from numpy import expand_dims
from keras_facenet import FaceNet
import pickle
from grvispp import Ui_MainWindow
import os
import time
import requests
from globalval import global_health_check
from typing import Dict
from threading import Thread

def get_employee_data(employee_id):
    # Construct the URL with the employee_id
    url = f'https://venus.hello-olzhas.kz/api/v1/employees/{employee_id}/'

    # Headers as per the provided curl command
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'GxFcOFW1RanWza01020vBKDVqmjucQif2nHJcuEHnWGhvZ5wg1F6WzkP4jyp4TJv'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON response if the request was successful
        return response.json()
    else:
        # Return an error message if something went wrong
        return {'error': f'Request failed with status code {response.status_code}'}

class LoadFaceNetThread(QThread):
    net_onload_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    def run(self):
        self.faceNet = FaceNet()
        self.net_onload_signal.emit(self.faceNet)


class VideoThread(QThread):
    face_recognized_signal = pyqtSignal(str)
    change_pixmap_signal = pyqtSignal(QImage)
    recognition_complete_signal = pyqtSignal(object)  # Changed from str to object
    request_timer_start = pyqtSignal()
    recognition_face_start = pyqtSignal()
    MyFaceNet = None

    def __init__(self):
        super().__init__()
        self.recognizing_faces = True
        self.recognized_face = None
        self.recognition_duration = 3000
        self._is_running = True
        self.cap = None
        self.thread_flag = False

    def update_database_from_folder(folder_path, database_path):
        # Initialize FaceNet
        facenet = FaceNet()

        # Load existing database or initialize a new one
        try:
            with open(database_path, "rb") as f:
                database = pickle.load(f)
        except (FileNotFoundError, EOFError):
            database = {}

        pass

        # Process each image in the folder
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder_path, filename)
                img = cv2.imread(img_path)
                img = cv2.resize(img, (160, 160))
                img = img[..., ::-1]  # Convert BGR to RGB
                img = np.asarray(img)
                img = expand_dims(img, axis=0)

                # Extract embedding and update database
                embedding = facenet.embeddings(img)
                database[filename] = embedding

        # Save the updated database
        with open(database_path, "wb") as f:
            pickle.dump(database, f)

    def is_face_size_sufficient(self, x, y, w, h, min_area_pixels):
        face_area = w * h
        return face_area >= min_area_pixels

    def find_closest_embedding(self, embedding, database):
        min_dist = float('inf')
        identity = None
        for (name, db_emb) in database.items():
            dist = np.linalg.norm(db_emb - embedding)
            if dist < min_dist:
                min_dist = dist
                identity = name
        confidence = max(0, 100 - (min_dist * 10))
        if confidence > 90:  # Confidence threshold
            return identity
        else:
            return "Unknown"

    def convert_cv_qt(self, cv_img):
        """Convert from an OpenCV image to QImage"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    
    def thread_funtion(self, net, face, database):
        self.thread_flag = True
        start = time.time()
        embedding = net.embeddings(face)
        identity = self.find_closest_embedding(embedding, database)
        if self.recognized_face != identity and identity != "Unknown":
            self.recognized_face = identity
            employee_id = identity.split('.')[0]
            employee_data = get_employee_data(employee_id)
            print(employee_id)
            if employee_data:
                self.recognition_complete_signal.emit(employee_data)  # Emitting dictionary directly
            else:
                self.thread_flag = False
        else:
            self.thread_flag = False

    def run(self):
        start_time = time.time()
        print("start: ", start_time)
        self._is_running = True  # Ensure the thread's loop can start/continue running
        self.cap = cv2.VideoCapture(0)  # Initialize the capture object


        # Load the face embeddings database
        with open("data.pkl", "rb") as f:
            database = pickle.load(f)

        # Initialize FaceNet
        # MyFaceNet = FaceNet()
        cascade_path = 'C:/Users/АСМО/PycharmProjects/ASMO/haarcascade_frontalface_default.xml'
        HaarCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Define a threshold for the minimum face area in pixels
        min_face_area_pixels = 32000  # Example threshold value, adjust based on calibration

        # Rectangle parameters
        rect_center = (225, 225)
        rect_width = 450
        rect_height = 450
        rect_x = rect_center[0] - rect_width // 2
        rect_y = rect_center[1] - rect_height // 2
        end_time = time.time()
        print("end_time: ", end_time, " take_time: ", end_time - start_time)
        while self._is_running and self.cap.isOpened():
            ret, cv_img = self.cap.read()
            if ret:
                # Flip the captured frame horizontally
                cv_img = cv2.flip(cv_img, 1)

                self.recognition_face_start.emit()
                if self.MyFaceNet is not None:
                    faces = HaarCascade.detectMultiScale(cv_img, 1.1, 4)
                    thread = Thread()

                    for (x, y, w, h) in faces:
                        # Check if face recognition is enabled and if the detected face meets the size criteria
                        if self.recognizing_faces and self.is_face_size_sufficient(x, y, w, h, min_face_area_pixels):
                            # Check if the face is within the specified rectangle
                            if rect_x < x < rect_x + rect_width and rect_y < y < rect_y + rect_height:
                                face = cv_img[y:y + h, x:x + w]
                                face = cv2.resize(face, (160, 160))
                                face = face[..., ::-1]  # Convert BGR to RGB
                                face = np.asarray(face)
                                face = expand_dims(face, axis=0)
                                if not self.thread_flag:
                                    thread = Thread(target=self.thread_funtion, args=(self.MyFaceNet, face, database))
                                    thread.start()

                            # Draw the rectangle and identity text on the frame
                            cv2.rectangle(cv_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # cv2.putText(cv_img, identity, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255),
                #             2)
                cv2.rectangle(cv_img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height),
                            (255, 0, 0), 2)  # Blue rectangle

                # Convert frame for Qt display and emit signal
                qt_img = self.convert_cv_qt(cv_img)
                self.change_pixmap_signal.emit(qt_img)
            else:
                break  # Break the loop if the frame is not properly captured

        # Release the camera and cleanup after the loop ends
        if self.cap:
            self.cap.release()
        print("Video capture stopped.")

    # Methods to control face recognition
    def pause_face_recognition(self):
        self.recognizing_faces = False

    def resume_face_recognition(self):
        self.recognizing_faces = True

    def stop(self):
        self._is_running = False
        if self.cap.isOpened():
            self.cap.release()
        QThread.quit(self)

class RecognizedFaceWindow(QWidget):
    def __init__(self, face_name):
        super().__init__()
        self.grvisWindow = None  # This will hold the reference to the grvis window
        self.setWindowTitle("Recognized Face")
        self.setGeometry(200, 200, 300, 200)

        # Create a label to display the recognized face name
        self.face_label = QLabel(self)
        self.face_label.setText("Recognized Face: " + face_name)
        self.face_label.setAlignment(Qt.AlignCenter)
        self.face_label.setGeometry(50, 50, 200, 100)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.grvisWindow = None  # Initialize here to ensure it's always defined

        self.setWindowTitle("Real-time Face Recognition")
        self.overlay_image_path = 'gui/gui2.png'
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.resize(self.size())
        self.overlay_label = QLabel(self)
        self.setup_overlay()


        self.thread = VideoThread()
        self.faceNetThread = LoadFaceNetThread()

        self.faceNetThread.net_onload_signal.connect(self.onload_faceNet)

        self.thread.change_pixmap_signal.connect(self.update_camera_feed)
        self.thread.face_recognized_signal.connect(self.start_recognition_timer)
        self.thread.recognition_complete_signal.connect(self.on_recognition_timer_timeout)
        self.overlay_image_path = 'gui/gui1.png'
        self.thread.recognition_face_start.connect(self.setup_overlay)
        self.thread.start()
        self.faceNetThread.start()

        self.thread.request_timer_start.connect(self.start_recognition_timer)  # Properly set up the connection once

        self.setFixedSize(1440,1024)
        self.show()
    
    @pyqtSlot(object)
    def onload_faceNet(self, faceNet):
        print('on_load')
        self.thread.MyFaceNet = faceNet

    def update_camera_feed(self, qt_img):
        # Set the pixmap for the camera feed
        pixmap = QPixmap.fromImage(qt_img)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def setup_overlay(self):
        # Load and set up the overlay image
        overlay_pixmap = QPixmap(self.overlay_image_path)
        if overlay_pixmap.isNull():
            print("Failed to load the overlay image.")
            sys.exit(-1)
        self.overlay_label.setPixmap(overlay_pixmap)
        self.overlay_label.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.overlay_label.setGeometry(0, 0, self.width(), self.height())  # Set geometry to cover the entire window
        self.overlay_label.setAttribute(Qt.WA_TranslucentBackground)

    @pyqtSlot()
    def start_recognition_timer(self):
        if not self.recognition_timer.isActive():  # Check if the timer is not already running
            self.recognition_timer.start(self.thread.recognition_duration)


    @pyqtSlot(object)
    def on_recognition_timer_timeout(self, employee_data):
        # Stop the timer to prevent it from triggering again
        if self.thread.recognized_face or self.thread.recognized_face != "Unknown":
            if employee_data:
                self.openGrvisWindowWithData(employee_data)
            else:
                print(f"No data found for employee")
        else:
            print("No recognized face data")

    def resizeEvent(self, event):
        # Resize event for the main window
        super().resizeEvent(event)
        self.image_label.resize(self.size())
        self.overlay_label.resize(self.size())
        self.overlay_label.setGeometry(0, 0, self.width(), self.height())  # Upd

    def closeEvent(self, event):
        # Terminate the video thread on window close
        self.thread.terminate()



    def closeWindowAndStopVideo(self):
        # Stop the VideoThread first to ensure resources are released properly
        if self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()  # Wait for the thread to finish

        # Then close the MainWindow
        self.close()

    def openGrvisWindowWithData(self, data):
        if self.grvisWindow is None or not self.grvisWindow.isVisible():
            self.grvisWindow = QMainWindow()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self.grvisWindow)
        else:
            self.grvisWindow.raise_()
            self.grvisWindow.activateWindow()

        self.ui.updateUIWithAPIData(data)
        self.grvisWindow.showFullScreen()
        print(global_health_check.checkup)

        # It's now safe to close the main window and stop the video after ensuring grvisWindow is displayed
        self.close()