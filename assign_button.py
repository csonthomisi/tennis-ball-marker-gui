from PySide2.QtWidgets import QPushButton


class AssignButton(QPushButton):
    def set_row_column(self, row, col):
        self.row = row
        self.column = col

    def get_row_column(self):
        return self.row, self.column

    def set_button_selected_status(self):
        self.setStyleSheet("background-color: green")
