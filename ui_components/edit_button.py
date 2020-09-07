from PySide2.QtWidgets import QPushButton


class EditButton(QPushButton):
    def set_row_column(self, row, col):
        self.row = row
        self.column = col

    def get_row_column(self):
        return self.row, self.column
