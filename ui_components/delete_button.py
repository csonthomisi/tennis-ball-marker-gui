from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QPushButton


class DeleteButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setIcon(QtGui.QIcon("delete.jpg"))
        self.setIconSize(QtCore.QSize(20, 20))

    def set_row_column(self, row, col):
        self.row = row
        self.column = col

    def get_row_column(self):
        return self.row, self.column
