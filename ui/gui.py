# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QLocale)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1130, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMouseTracking(True)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.calc_homography_btn = QPushButton(self.centralwidget)
        self.calc_homography_btn.setObjectName(u"calc_homography_btn")
        self.calc_homography_btn.setEnabled(True)
        self.calc_homography_btn.setGeometry(QRect(10, 660, 160, 30))
        sizePolicy.setHeightForWidth(self.calc_homography_btn.sizePolicy().hasHeightForWidth())
        self.calc_homography_btn.setSizePolicy(sizePolicy)
        self.image_holder = QLabel(self.centralwidget)
        self.image_holder.setObjectName(u"image_holder")
        self.image_holder.setEnabled(True)
        self.image_holder.setGeometry(QRect(300, 10, 850, 680))
        sizePolicy.setHeightForWidth(self.image_holder.sizePolicy().hasHeightForWidth())
        self.image_holder.setSizePolicy(sizePolicy)
        self.image_holder.setMouseTracking(True)
        self.image_holder.setAcceptDrops(False)
        self.image_holder.setAlignment(Qt.AlignCenter)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 10, 280, 520))
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 100))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 278, 518))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMinimumSize(QSize(0, 200))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QRect(10, 620, 160, 30))
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.road_unit = QDoubleSpinBox(self.centralwidget)
        self.road_unit.setObjectName(u"road_unit")
        self.road_unit.setGeometry(QRect(180, 620, 110, 30))
        sizePolicy.setHeightForWidth(self.road_unit.sizePolicy().hasHeightForWidth())
        self.road_unit.setSizePolicy(sizePolicy)
        self.road_unit.setValue(1.000000000000000)
        self.zoom_image = QPushButton(self.centralwidget)
        self.zoom_image.setObjectName(u"zoom_image")
        self.zoom_image.setGeometry(QRect(10, 580, 280, 30))
        self.select_image_btn = QPushButton(self.centralwidget)
        self.select_image_btn.setObjectName(u"select_image_btn")
        self.select_image_btn.setGeometry(QRect(10, 540, 280, 30))
        sizePolicy.setHeightForWidth(self.select_image_btn.sizePolicy().hasHeightForWidth())
        self.select_image_btn.setSizePolicy(sizePolicy)
        self.imu = QCheckBox(self.centralwidget)
        self.imu.setObjectName(u"imu")
        self.imu.setGeometry(QRect(180, 660, 50, 30))
        self.utm = QCheckBox(self.centralwidget)
        self.utm.setObjectName(u"utm")
        self.utm.setGeometry(QRect(240, 660, 50, 30))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.calc_homography_btn.setText(QCoreApplication.translate("MainWindow", u"Calculate Homography", None))
        self.image_holder.setText(QCoreApplication.translate("MainWindow", u"Upload an Image", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Road Unit", None))
        self.zoom_image.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.select_image_btn.setText(QCoreApplication.translate("MainWindow", u"Browse an Image", None))
        self.imu.setText(QCoreApplication.translate("MainWindow", u"IMU", None))
        self.utm.setText(QCoreApplication.translate("MainWindow", u"UTM", None))
    # retranslateUi

