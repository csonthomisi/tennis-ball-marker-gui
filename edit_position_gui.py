from PySide2.QtWidgets import QDialog

from ui.edit import Ui_Dialog


class EditPositionGUI(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.x = None
        self.y = None
        self.prev_x = None
        self.prev_y = None
        self.r = None
        self.c = None

    def set_ball_position(self, x, y, r, c):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.prev_x = x
        self.prev_y = y
        self.edit_row_value.setText(str(r))
        self.edit_x_value.setText(str(x))
        self.edit_y_value.setText(str(y))
        self.edit_column_value.setText(str(c))
        self.buttonBox.accepted.connect(self.on_save_click)
        self.buttonBox.rejected.connect(self.on_cancel_click)

    def get_x_y(self):
        return self.x, self.y

    def get_prev_x_y(self):
        return self.prev_x, self.prev_y

    def on_save_click(self):
        self.x = float(self.edit_x_value.text())
        self.y = float(self.edit_y_value.text())
        self.close()

    def on_cancel_click(self):
        self.close()
