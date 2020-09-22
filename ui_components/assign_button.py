from PySide2.QtWidgets import QPushButton


class AssignButton(QPushButton):
    def set_row_column(self, row, col):
        self.row = row
        self.column = col
        self.selected = False

    def get_row_column(self):
        return self.row, self.column

    def is_selected(self):
        return self.selected

    def set_button_status_selected(self):
        self.selected = True
        self.setStyleSheet("background-color: green")

    def set_button_status_default(self):
        self.selected = False
        self.setStyleSheet("background-color: light gray")
