from PySide2.QtWidgets import QPushButton


class AssignButton(QPushButton):
    def set_row_column(self, row, col):
        self.row = row
        self.column = col

    def get_row_column(self):
        return self.row, self.column

    def set_button_status_selected(self):
        self.setStyleSheet("background-color: green")

    def set_button_status_default(self):
        self.setStyleSheet("background-color: light gray")
