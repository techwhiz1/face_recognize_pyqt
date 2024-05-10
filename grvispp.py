
from PyQt5 import QtCore, QtGui, QtWidgets
from globalval import global_health_check
import serial
import threading
import requests
import datetime
import time
import cv2
import numpy as np

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QUrl
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import urllib


class Ui_MainWindow(object):

    def __init__(self):
            # Initialize latestData to an empty dictionary or None
            self.latestData = None
            self.initiateSerialCommunication()
    def setupUi(self, MainWindow):
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width() - 40

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, int(self.height * 0.02), int(self.width * 0.4), int(self.height * 0.6)))
        self.frame.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.avatar = QtWidgets.QLabel(self.frame)
        self.avatar.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.avatar.setGeometry(int(self.frame.width() * 0.3), 0, int(self.frame.width() * 0.4), int(self.frame.height() * 0.4))  # Set geometry to cover the entire window
        self.avatar.setAttribute(Qt.WA_TranslucentBackground)
        
        self.pasteHereName = QtWidgets.QLabel(self.frame)
        self.pasteHereName.setGeometry(QtCore.QRect(int(self.frame.width() * 0.2), int(self.frame.height() * 0.35), int(self.frame.width() * 0.6), int(self.frame.height() * 0.2)))
        self.pasteHereName.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.pasteHereName.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pasteHereName.setFont(font)
        self.pasteHereName.setObjectName("pasteHereName")
        self.valCity = QtWidgets.QLabel(self.frame)
        self.valCity.setGeometry(QtCore.QRect(int(self.frame.width() * 0.35), int(self.frame.height() * 0.5), int(self.frame.width() * 0.3), int(self.frame.height() * 0.15)))
        self.valCity.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.location_icon = QtWidgets.QLabel(self.frame)
        pixmap = QPixmap("icons/Location_Icon.png")
        self.location_icon.setPixmap(pixmap)
        self.location_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.location_icon.setGeometry(int(self.frame.width() * 0.4), int(self.frame.height() * 0.53), 60, 60)  # Set geometry to cover the entire window
        self.location_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.valCity.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.valCity.setFont(font)
        self.valCity.setObjectName("valCity")
        # self.label_3 = QtWidgets.QLabel(self.frame)
        # self.label_3.setGeometry(QtCore.QRect(160, 400, 100, 100))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        # self.label_3.setPalette(palette)
        # font = QtGui.QFont()
        # font.setFamily("Microsoft YaHei UI Light")
        # font.setPointSize(14)
        # self.label_3.setFont(font)
        # self.label_3.setObjectName("label_3")
        self.valUdost = QtWidgets.QLabel(self.frame)
        self.valUdost.setGeometry(QtCore.QRect(0, int(self.frame.height() * 0.7), int(self.frame.width() * 0.33), int(self.frame.height() * 0.3)))
        self.valUdost.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valUdost.setPalette(palette)
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.valUdost.setFont(font)
        self.valUdost.setObjectName("valUdost")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(0, int(self.frame.height() * 0.6), int(self.frame.width() * 0.33), int(self.frame.height() * 0.15)))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_5.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(int(self.frame.width() * 0.33), int(self.frame.height() * 0.6), int(self.frame.width() * 0.33), int(self.frame.height() * 0.15)))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_6.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(int(self.frame.width() * 0.66), int(self.frame.height() * 0.6), int(self.frame.width() * 0.33), int(self.frame.height() * 0.15)))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_7.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.valOrganization = QtWidgets.QLabel(self.frame)
        self.valOrganization.setWordWrap(True)
        self.valOrganization.setGeometry(QtCore.QRect(int(self.frame.width() * 0.33), int(self.frame.height() * 0.7), int(self.frame.width() * 0.33), int(self.frame.height() * 0.3)))
        self.valOrganization.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valOrganization.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.valOrganization.setFont(font)
        self.valOrganization.setObjectName("valOrganization")
        self.valJob = QtWidgets.QLabel(self.frame)
        self.valJob.setWordWrap(True)
        self.valJob.setGeometry(QtCore.QRect(int(self.frame.width() * 0.66), int(self.frame.height() * 0.7), int(self.frame.width() * 0.33), int(self.frame.height() * 0.3)))
        self.valJob.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valJob.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.valJob.setFont(font)
        self.valJob.setObjectName("valJob")
        self.Temperature = QtWidgets.QFrame(self.centralwidget)
        self.Temperature.setGeometry(QtCore.QRect(int(self.width * 0.42), int(self.height * 0.02), int(self.width * 0.29), int(self.height * 0.19)))
        self.Temperature.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.Temperature.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Temperature.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Temperature.setObjectName("Temperature")
        self.temprature_icon = QtWidgets.QLabel(self.Temperature)
        pixmap = QPixmap("icons/Temprature.png")
        self.temprature_icon.setPixmap(pixmap)
        self.temprature_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.temprature_icon.setGeometry(0, int(self.Temperature.height() * 0.2), int(self.Temperature.height() * 0.6), int(self.Temperature.height() * 0.6))  # Set geometry to cover the entire window
        self.temprature_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.label_14 = QtWidgets.QLabel(self.Temperature)
        self.label_14.setGeometry(QtCore.QRect(int(self.Temperature.width() * 0.3), int(self.Temperature.height() * 0.1), int(self.Temperature.width() * 0.75), int(self.Temperature.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_14.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.valTemp = QtWidgets.QLabel(self.Temperature)
        self.valTemp.setGeometry(QtCore.QRect(int(self.Temperature.width() * 0.3), int(self.Temperature.height() * 0.5), int(self.Temperature.width() * 0.75), int(self.Temperature.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valTemp.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valTemp.setFont(font)
        self.valTemp.setObjectName("valTemp")
        self.valTemp.raise_()
        self.label_14.raise_()
        self.pulse = QtWidgets.QFrame(self.centralwidget)
        self.pulse.setGeometry(QtCore.QRect(int(self.width * 0.42), int(self.height * 0.225), int(self.width * 0.29), int(self.height * 0.19)))
        self.pulse.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.pulse.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pulse.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pulse.setObjectName("pulse")
        self.pulse_icon = QtWidgets.QLabel(self.pulse)
        pixmap = QPixmap("icons/Pulse.png")
        self.pulse_icon.setPixmap(pixmap)
        self.pulse_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.pulse_icon.setGeometry(0, int(self.pulse.height() * 0.2), int(self.pulse.height() * 0.6), int(self.pulse.height() * 0.6))  # Set geometry to cover the entire window
        self.pulse_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.label_15 = QtWidgets.QLabel(self.pulse)
        self.label_15.setGeometry(QtCore.QRect(int(self.pulse.width() * 0.3), int(self.pulse.height() * 0.1), int(self.pulse.width() * 0.75), int(self.pulse.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_15.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.valPulse = QtWidgets.QLabel(self.pulse)
        self.valPulse.setGeometry(QtCore.QRect(int(self.pulse.width() * 0.3), int(self.pulse.height() * 0.5), int(self.pulse.width() * 0.75), int(self.pulse.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valPulse.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valPulse.setFont(font)
        self.valPulse.setObjectName("valPulse")
        self.valPulse.raise_()
        self.label_15.raise_()
        self.pressure = QtWidgets.QFrame(self.centralwidget)
        self.pressure.setGeometry(QtCore.QRect(QtCore.QRect(int(self.width * 0.42), int(self.height * 0.43), int(self.width * 0.29), int(self.height * 0.19))))
        self.pressure.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.pressure.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pressure.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pressure.setObjectName("pressure")
        self.pressure_icon = QtWidgets.QLabel(self.pressure)
        pixmap = QPixmap("icons/Pressure.png")
        self.pressure_icon.setPixmap(pixmap)
        self.pressure_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.pressure_icon.setGeometry(0, int(self.pressure.height() * 0.2), int(self.pressure.height() * 0.6), int(self.pressure.height() * 0.6))  # Set geometry to cover the entire window
        self.pressure_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.label_16 = QtWidgets.QLabel(self.pressure)
        self.label_16.setGeometry(QtCore.QRect(int(self.pressure.width() * 0.3), int(self.pressure.height() * 0.1), int(self.pressure.width() * 0.75), int(self.pressure.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_16.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.valPressure = QtWidgets.QLabel(self.pressure)
        self.valPressure.setGeometry(QtCore.QRect(int(self.pressure.width() * 0.3), int(self.pressure.height() * 0.5), int(self.pressure.width() * 0.75), int(self.pressure.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valPressure.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valPressure.setFont(font)
        self.valPressure.setObjectName("valPressure")
        self.valPressure.raise_()
        self.label_16.raise_()
        self.alcometer = QtWidgets.QFrame(self.centralwidget)
        self.alcometer.setGeometry(QtCore.QRect(QtCore.QRect(int(self.width * 0.72), int(self.height * 0.02), int(self.width * 0.29), int(self.height * 0.19))))
        self.alcometer.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.alcometer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.alcometer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.alcometer.setObjectName("alcometer")
        self.breathalyzer_icon = QtWidgets.QLabel(self.alcometer)
        pixmap = QPixmap("icons/Breathalyzer.png")
        self.breathalyzer_icon.setPixmap(pixmap)
        self.breathalyzer_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.breathalyzer_icon.setGeometry(QtCore.QRect(0, int(self.pressure.height() * 0.2), int(self.pressure.height() * 0.6), int(self.pressure.height() * 0.6)))  # Set geometry to cover the entire window
        self.breathalyzer_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.label_17 = QtWidgets.QLabel(self.alcometer)
        self.label_17.setGeometry(QtCore.QRect(int(self.pressure.width() * 0.3), int(self.pressure.height() * 0.1), int(self.pressure.width() * 0.75), int(self.pressure.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_17.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.valAlc = QtWidgets.QLabel(self.alcometer)
        self.valAlc.setGeometry(QtCore.QRect(int(self.pressure.width() * 0.3), int(self.pressure.height() * 0.5), int(self.pressure.width() * 0.75), int(self.pressure.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valAlc.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valAlc.setFont(font)
        self.valAlc.setObjectName("valAlc")
        self.valAlc.raise_()
        self.label_17.raise_()
        self.narcotest = QtWidgets.QFrame(self.centralwidget)
        self.narcotest.setGeometry(QtCore.QRect(QtCore.QRect(int(self.width * 0.72), int(self.height * 0.225), int(self.width * 0.29), int(self.height * 0.19))))
        self.narcotest.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.narcotest.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.narcotest.setFrameShadow(QtWidgets.QFrame.Raised)
        self.narcotest.setObjectName("narcotest")
        self.drug_icon = QtWidgets.QLabel(self.narcotest)
        pixmap = QPixmap("icons/Drug_Test.png")
        self.drug_icon.setPixmap(pixmap)
        self.drug_icon.setScaledContents(True)  # Ensure the pixmap scales with the label
        self.drug_icon.setGeometry(QtCore.QRect(0, int(self.narcotest.height() * 0.2), int(self.narcotest.height() * 0.6), int(self.narcotest.height() * 0.6)))  # Set geometry to cover the entire window
        self.drug_icon.setAttribute(Qt.WA_TranslucentBackground)
        self.label_19 = QtWidgets.QLabel(self.narcotest)
        self.label_19.setGeometry(QtCore.QRect(int(self.narcotest.width() * 0.3), int(self.narcotest.height() * 0.1), int(self.narcotest.width() * 0.75), int(self.narcotest.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_19.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.valNarc = QtWidgets.QLabel(self.narcotest)
        self.valNarc.setGeometry(QtCore.QRect(int(self.narcotest.width() * 0.3), int(self.narcotest.height() * 0.5), int(self.narcotest.width() * 0.75), int(self.narcotest.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valNarc.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valNarc.setFont(font)
        self.valNarc.setObjectName("valNarc")
        self.valNarc.raise_()
        self.label_19.raise_()
        self.zhaloby = QtWidgets.QFrame(self.centralwidget)
        self.zhaloby.setGeometry(QtCore.QRect(QtCore.QRect(int(self.width * 0.72), int(self.height * 0.43), int(self.width * 0.29), int(self.height * 0.19))))
        self.zhaloby.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.zhaloby.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.zhaloby.setFrameShadow(QtWidgets.QFrame.Raised)
        self.zhaloby.setObjectName("zhaloby")
        self.label_21 = QtWidgets.QLabel(self.zhaloby)
        self.label_21.setGeometry(QtCore.QRect(int(self.zhaloby.width() * 0.3), int(self.zhaloby.height() * 0.1), int(self.zhaloby.width() * 0.75), int(self.zhaloby.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(163, 174, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_21.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.valZhal = QtWidgets.QLabel(self.zhaloby)
        self.valZhal.setGeometry(QtCore.QRect(int(self.zhaloby.width() * 0.3), int(self.zhaloby.height() * 0.5), int(self.zhaloby.width() * 0.75), int(self.zhaloby.height() * 0.45)))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.valZhal.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.valZhal.setFont(font)
        self.valZhal.setObjectName("valZhal")
        self.valZhal.raise_()
        self.label_21.raise_()
        self.frame_8 = QtWidgets.QFrame(self.centralwidget)
        self.frame_8.setGeometry(QtCore.QRect(20, int(self.height * 0.64), self.width, int(self.height * 0.34)))
        self.frame_8.setStyleSheet("QWidget {\n"
"    border-radius: 15px; /* Adjust for rounded corners */\n"
"    background-color: white; /* Background color */\n"
"    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15); /* Drop shadow effect */\n"
"    padding: 20px; /* Space inside the frame */\n"
"}\n"
"")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.label_24 = QtWidgets.QLabel(self.frame_8)
        self.label_24.setGeometry(QtCore.QRect(int(self.frame_8.width() * 0.3), int(self.frame_8.height() * 0.2), int(self.frame_8.width() * 0.4), int(self.frame_8.height() * 0.3)))
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(27, 37, 89))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_24.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.buttonYes = QtWidgets.QPushButton(self.frame_8)
        self.buttonYes.setGeometry(QtCore.QRect(int(self.frame_8.width() * 0.2), int(self.frame_8.height() * 0.55), int(self.frame_8.width() * 0.29), int (self.frame_8.height() * 0.38)))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.buttonYes.setFont(font)
        self.buttonYes.setMouseTracking(True)
        self.buttonYes.setTabletTracking(True)
        self.buttonYes.setStyleSheet("QPushButton {\n"
"    background-color: #6858ff; /* Замените на точный цвет вашей кнопки */\n"
"    color: white; /* Цвет текста */\n"
"    border-radius: 15px; /* Радиус скругления углов, подгоните под ваш дизайн */\n"
"    padding: 10px 20px; /* Отступы внутри кнопки */\n"
"    font-size: 50px; /* Размер шрифта */\n"
"    font-weight: bold; /* Жирность шрифта */\n"
"    text-align: center; /* Выравнивание текста по центру */\n"
"    border: none; /* Убираем стандартный бордюр */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:#6858ff; /* Цвет кнопки при наведении, подберите по вашему дизайну */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #6858ff; /* Цвет кнопки при нажатии, подберите по вашему дизайну */\n"
"}\n"
"")
        self.buttonYes.setObjectName("buttonYes")
        self.buttonNo = QtWidgets.QPushButton(self.frame_8)
        self.buttonNo.setGeometry(QtCore.QRect(int(self.frame_8.width() * 0.51), int(self.frame_8.height() * 0.55), int(self.frame_8.width() * 0.29), int (self.frame_8.height() * 0.38)))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.buttonNo.setFont(font)
        self.buttonNo.setMouseTracking(True)
        self.buttonNo.setTabletTracking(True)
        self.buttonNo.setStyleSheet("QPushButton {\n"
"    background-color: #6858ff; /* Замените на точный цвет вашей кнопки */\n"
"    color: white; /* Цвет текста */\n"
"    border-radius: 15px; /* Радиус скругления углов, подгоните под ваш дизайн */\n"
"    padding: 10px 20px; /* Отступы внутри кнопки */\n"
"    font-size: 50px; /* Размер шрифта */\n"
"    font-weight: bold; /* Жирность шрифта */\n"
"    text-align: center; /* Выравнивание текста по центру */\n"
"    border: none; /* Убираем стандартный бордюр */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #6858ff; /* Цвет кнопки при наведении, подберите по вашему дизайну */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:#6858ff; /* Цвет кнопки при нажатии, подберите по вашему дизайну */\n"
"}\n"
"")
        self.buttonNo.setObjectName("buttonNo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.buttonNo.clicked.connect(self.buttonNoClicked)

        self.buttonYes.setObjectName("buttonYes")
        MainWindow.setCentralWidget(self.centralwidget)
        self.buttonYes.clicked.connect(self.buttonYesClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.additionalButton = QtWidgets.QPushButton(self.frame_8)
        self.additionalButton.setGeometry(QtCore.QRect(550, 160, 700, 160))  # Same geometry as buttonYes
        self.additionalButton.setFont(QtGui.QFont("MS Shell Dlg 2", -1, True, 75))
        self.additionalButton.setStyleSheet("""
                    QPushButton {
                        background-color: #6858ff;
                        color: white;
                        border-radius: 15px;
                        padding: 10px 20px;
                        font-size: 50px;
                        font-weight: bold;
                        text-align: center;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #7a6eff;
                    }
                    QPushButton:pressed {
                        background-color: #5648cf;
                    }
                """)
        self.additionalButton.setText("Подписать и отправить")
        self.additionalButton.clicked.connect(self.additionalActionClicked)
        self.additionalButton.hide()  # Initially hidden

        self.additionalButton2 = QtWidgets.QPushButton(self.frame_8)
        self.additionalButton2.setGeometry(QtCore.QRect(550, 160, 700, 160))  # Adjust the geometry as needed
        self.additionalButton2.setFont(QtGui.QFont("MS Shell Dlg 2", -1, True, 75))
        self.additionalButton2.setStyleSheet("""
            QPushButton {
                background-color: #6858ff;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 50px;
                font-weight: bold;
                text-align: center;
                border: none;
            }
            QPushButton:hover {
                background-color: #7a6eff;
            }
            QPushButton:pressed {
                background-color: #5648cf;
            }
        """)
        self.additionalButton2.setText("Подписать и отправить")
        self.additionalButton2.clicked.connect(self.additionalAction2Clicked)
        self.additionalButton2.hide()  # Initially hidden






    def additionalActionClicked(self):
            print("Additional button clicked")
            # Call the post_health_status function with specified parameters
            post_health_status(temperature=str(global_health_check.temp), pulse="99", pressure="170",
                               breathalyzer=str(global_health_check.alcot), drug_test=str(global_health_check.narcot),
                               complaints=str(global_health_check.zhaloby), dopusk=1,
                               employee=str(global_health_check.iin))
            self.additionalButton.hide()

    def additionalAction2Clicked(self):
            print("Additional Action 2 button clicked")
            post_health_status(temperature=str(global_health_check.temp), pulse="99", pressure="170",
                               breathalyzer=str(global_health_check.alcot), drug_test=str(global_health_check.narcot),
                               complaints=str(global_health_check.zhaloby), dopusk=0,
                               employee=str(global_health_check.iin))
            self.additionalButton2.hide()


    def initiateSerialCommunication(self):
            # Run the communication in a separate thread to avoid blocking the UI
            threading.Thread(target=self.communicateWithSerialPort, daemon=True).start()

    def buttonYesClicked(self):
            print("111")
            # Change color of zhaloby to red
            self.zhaloby.setStyleSheet("background-color: rgb(190,77,37);")
            # Disappear both buttons
            self.buttonYes.hide()
            self.buttonNo.hide()
            # Change text of label_24 to "GOGO"
            self.label_24.setText("Подуйте в алкометр")
            # Change text of valZhal to "Yes"
            self.valZhal.setText("Да")
            print("Жалобы")
            global_health_check.zhaloby = 0
            print(global_health_check.zhaloby)
    def buttonNoClicked(self):
            print("222")
            # Change color of zhaloby to green
            self.zhaloby.setStyleSheet("background-color: rgb(150, 190, 37);")
            self.buttonYes.hide()
            self.buttonNo.hide()
            # Change text of label_24 to "NONO"
            self.label_24.setText("Подуйте в алкометр")
            # Change text of valZhal to "No"
            self.valZhal.setText("Нет")
            print("Жалобы")
            global_health_check.zhaloby = 1
            print(global_health_check.zhaloby)


    def communicateWithSerialPort(self):
            try:
                    with serial.Serial('COM3', 4800, timeout=1) as ser:
                            # Sending command
                            ser.write(b"$FASTSENTECH\r\n")

                            # Waiting for response from COM8
                            while True:
                                    line = ser.readline().decode().strip()  # Read a line and strip it of whitespace
                                    if line == '$R:PASS':
                                            self.valAlc.setText("Пройден")
                                            self.alcometer.setStyleSheet("background-color: rgb(150, 190, 37);")
                                            global_health_check.alcot = 1
                                            print(global_health_check.alcot)
                                            break
                                    elif line == '$R:FAIL':
                                            self.valAlc.setText("Не пройден")
                                            self.alcometer.setStyleSheet("background-color: rgb(190,77,37);")
                                            global_health_check.alcot = 0
                                            print(global_health_check.alcot)
                                            break

                    # Update label_24 text as per the new requirement
                    self.label_24.setText("Наденьте шлем")
                    time.sleep(1)

                    # Now, handling temperature data from COM5
                    with serial.Serial('COM4', 9600, timeout=1) as ser:
                            while True:
                                    command = 'TEMP'
                                    ser.write(f"{command}\r\n".encode())
                                    line = ser.readline().decode('utf-8').strip()
                                    if line and line.startswith("Temp:"):
                                            temp_data = line.split(':')[1]
                                            global_health_check.temp = float(temp_data)
                                            print(temp_data)
                                            break
                            print(temp_data)
                            bbal = temp_data
                            if(float(bbal) > 38):
                                    self.Temperature.setStyleSheet("background-color: rgb(190,77,37);")
                            else:
                                    self.Temperature.setStyleSheet("background-color: rgb(150, 190, 37);")
                            global_health_check.temp = temp_data
                            self.valTemp.setText(temp_data)
                            self.detectCircleRadius()

            except serial.SerialException as e:
                    print(f"Error in serial communication: {e}")

    def detectCircleRadius(self):
            def display_circle_size(img, circle, color):
                    cv2.circle(img, (circle[0], circle[1]), circle[2], color, 2)
                    cv2.putText(img, f"r={circle[2]}", (circle[0] - 100, circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color, 2)
                    print(f"Circle radius: {circle[2]} pixels")
                    if (circle[2]>55):
                            print(55)
                            self.valNarc.setText("Не пройден")
                            self.narcotest.setStyleSheet("background-color: rgb(190,77,37);")
                            global_health_check.narcot=0
                            print(global_health_check.narcot)
                            self.isDopusk()


                    else:
                            print(45)
                            self.valNarc.setText("Пройден")
                            self.narcotest.setStyleSheet("background-color: rgb(150, 190, 37);")
                            global_health_check.narcot=1
                            print(global_health_check.narcot)
                            self.isDopusk()





                    return circle[2]


            cap = cv2.VideoCapture(0)  # Adjust the device index as per your setup
            if not cap.isOpened():
                    print("Error: Could not open camera.")
                    return

            radius_data_collected = False

            try:
                    while True and not radius_data_collected:
                            ret, frame = cap.read()
                            if not ret:
                                    print("Error: Can't receive frame. Exiting ...")
                                    break

                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            blur = cv2.GaussianBlur(gray, (9, 9), 0)

                            pupil_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                                                             param1=50, param2=30, minRadius=20, maxRadius=50)

                            if pupil_circles is not None:
                                    pupil_circles = np.round(pupil_circles[0, :]).astype("int")
                                    radius = display_circle_size(frame, pupil_circles[0], (255, 0, 0))
                                    radius_data_collected = True

                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
            finally:
                    cap.release()
                    cv2.destroyAllWindows()

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            # Static fields
            self.valUdost.setText(_translate("MainWindow", "800808559010"))
            self.label_7.setText(_translate("MainWindow", "Должность"))
            self.label_6.setText(_translate("MainWindow", "Организация"))
            self.label_5.setText(_translate("MainWindow", "Город"))
            self.label_14.setText(_translate("MainWindow", "Температура"))
            self.label_14.setStyleSheet("QLabel { color: black; }")
            self.valTemp.setText(_translate("MainWindow", "-"))
            self.valPulse.setText(_translate("MainWindow", "-"))
            self.label_15.setText(_translate("MainWindow", "Пульс"))
            self.label_15.setStyleSheet("QLabel { color: black; }")
            self.valPressure.setText(_translate("MainWindow", "-"))
            self.label_16.setText(_translate("MainWindow", "Давление"))
            self.label_16.setStyleSheet("QLabel { color: black; }")
            self.valAlc.setText(_translate("MainWindow", "-"))
            self.label_17.setText(_translate("MainWindow", "Алкометр"))
            self.label_17.setStyleSheet("QLabel { color: black; }")
            self.valNarc.setText(_translate("MainWindow", "-"))
            self.label_19.setText(_translate("MainWindow", "Наркотест"))
            self.label_19.setStyleSheet("QLabel { color: black; }")
            self.valZhal.setText(_translate("MainWindow", "Нет"))
            self.label_21.setText(_translate("MainWindow", "Жалобы"))
            self.label_21.setStyleSheet("QLabel { color: black; }")
            self.label_24.setText(_translate("MainWindow", "Наличие жалоб"))
            self.buttonYes.setText(_translate("MainWindow", "Да"))
            self.buttonNo.setText(_translate("MainWindow", "Нет"))

            # Dynamically updated fields
            if self.latestData:
                    self.updateDynamicFields(self.latestData, _translate)

    def updateUIWithAPIData(self, data):

            self.latestData = data  # Store the latest data
            _translate = QtCore.QCoreApplication.translate
            print("Updating UI with data:", data)

            """Update the UI elements with data from the API."""
            _translate = QtCore.QCoreApplication.translate
            self.pasteHereName.setText(_translate("MainWindow",
                                                  f"<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; vertical-align:sub;\">{data['full_name']}</span></p></body></html>"))
            city = str(data.get('city_name',
                                'Unknown City'))  # Convert to string and provides a default value if 'city' is not in data
            self.valCity.setText(_translate("MainWindow", city))

            # Convert 'organization' and 'position' to strings
            organization = str(data.get('organization_name', 'Unknown Organization'))
            position = str(data.get('position_name', 'Unknown Position'))
            iin = str(data.get('iin', 'Unknown iim'))
            global_health_check.iin = iin
            global_health_check.iin = str(data.get('iin', 'Unknown iim'))
            avatar = str(data.get('avatar', 'Unknown avatar'))
            if avatar == 'None':
                    avatar_pixmap = 'icons/user.jpeg'
                    rounded_pixmap = QPixmap(avatar_pixmap)
            else :
                response = requests.get(avatar)
                image_data = response.content 
                avatar_pixmap = QPixmap()
                avatar_pixmap.loadFromData(image_data)

                rounded_pixmap = QPixmap(avatar_pixmap.size())
                rounded_pixmap.fill(Qt.transparent)
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QtGui.QPainter.Antialiasing)
                painter.setBrush(QtGui.QBrush(avatar_pixmap))
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(avatar_pixmap.rect(), 300, 300)
                painter.end()
    
            self.avatar.setPixmap(rounded_pixmap)

            self.valUdost.setText(_translate("MainWindow", iin))

            self.valOrganization.setText(_translate("MainWindow", organization))
            self.valJob.setText(_translate("MainWindow", position))

    def isDopusk(self):
            if(global_health_check.zhaloby == 1 and global_health_check.narcot == 1 and global_health_check.alcot == 1 and (float(global_health_check.temp) <38) ):
                    print("Dopushen")
                    self.label_24.setText("Вы допущены")
                    self.additionalButton.show()  # Show the additional button



            else:
                    print("Nedopusk")
                    self.label_24.setText("Вы не допущены")
                    self.additionalButton2.show()

def post_health_status(temperature, pulse, pressure, breathalyzer, drug_test, complaints, dopusk, employee):
            url = "https://venus.hello-olzhas.kz/api/v1/health-status/"

            # Use the datetime library to get the current date and time in ISO format
            current_datetime = datetime.datetime.now().isoformat()

            payload = {
                    "date": current_datetime,
                    "temperature": temperature,
                    "pulse": pulse,
                    "pressure": pressure,
                    "breathalyzer": breathalyzer,
                    "drug_test": drug_test,
                    "complaints": complaints,
                    "edit_date": current_datetime,
                    "dopusk": dopusk,
                    "employee": employee
            }

            headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "X-CSRFToken": "DGjmaS1SU9OrDkmi5o6IkNtt6Da4xpyGZwlTyHJyqV7Mz9rNlnLjFCanKApZpsZW"
            }

            response = requests.post(url, json=payload, headers=headers)

            # Check the response status code to see if the request was successful
            if response.status_code == 200:
                    print("Success:", response.text)
            else:
                    print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
