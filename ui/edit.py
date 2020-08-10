# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 260)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 210, 280, 30))
        self.buttonBox.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.edit_row_line = QLineEdit(Dialog)
        self.edit_row_line.setObjectName(u"edit_row_line")
        self.edit_row_line.setEnabled(False)
        self.edit_row_line.setGeometry(QRect(20, 20, 100, 30))
        self.edit_row_line.setAlignment(Qt.AlignCenter)
        self.edit_row_value = QLineEdit(Dialog)
        self.edit_row_value.setObjectName(u"edit_row_value")
        self.edit_row_value.setEnabled(False)
        self.edit_row_value.setGeometry(QRect(140, 20, 160, 30))
        self.edit_column_line = QLineEdit(Dialog)
        self.edit_column_line.setObjectName(u"edit_column_line")
        self.edit_column_line.setEnabled(False)
        self.edit_column_line.setGeometry(QRect(20, 60, 100, 30))
        self.edit_column_line.setAlignment(Qt.AlignCenter)
        self.edit_column_value = QLineEdit(Dialog)
        self.edit_column_value.setObjectName(u"edit_column_value")
        self.edit_column_value.setEnabled(False)
        self.edit_column_value.setGeometry(QRect(140, 60, 160, 30))
        self.edit_x_line = QLineEdit(Dialog)
        self.edit_x_line.setObjectName(u"edit_x_line")
        self.edit_x_line.setEnabled(False)
        self.edit_x_line.setGeometry(QRect(20, 100, 100, 30))
        self.edit_x_line.setAlignment(Qt.AlignCenter)
        self.edit_x_value = QLineEdit(Dialog)
        self.edit_x_value.setObjectName(u"edit_x_value")
        self.edit_x_value.setGeometry(QRect(140, 100, 160, 30))
        self.edit_y_line = QLineEdit(Dialog)
        self.edit_y_line.setObjectName(u"edit_y_line")
        self.edit_y_line.setEnabled(False)
        self.edit_y_line.setGeometry(QRect(20, 140, 100, 30))
        self.edit_y_line.setAlignment(Qt.AlignCenter)
        self.edit_y_value = QLineEdit(Dialog)
        self.edit_y_value.setObjectName(u"edit_y_value")
        self.edit_y_value.setGeometry(QRect(140, 140, 160, 30))

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(Dialog.accept)
        # self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.edit_row_line.setText(QCoreApplication.translate("Dialog", u"row", None))
        self.edit_column_line.setText(QCoreApplication.translate("Dialog", u"column", None))
        self.edit_x_line.setText(QCoreApplication.translate("Dialog", u"x", None))
        self.edit_y_line.setText(QCoreApplication.translate("Dialog", u"y", None))
    # retranslateUi

