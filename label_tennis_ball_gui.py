from PySide2.QtCore import QRect
from PySide2.QtGui import QPixmap, Qt, QPainter, QPen
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

from assign_button import AssignButton
from edit_button import EditButton
from edit_position_gui import EditPositionGUI
from tennis_ball import TennisBall
from ui.gui import Ui_MainWindow
import csv
import numpy as np


class LabelTennisBallGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.edit_dialog = EditPositionGUI()
        self.add_buttons()
        self.select_image_btn.clicked.connect(self.browse_image)
        self.calc_homography_btn.clicked.connect(self.calculate_homography)
        self.save_btn.clicked.connect(self.save_balls)
        self.image_holder.mousePressEvent = self.get_ball_pixel_position

        self.clicked_x_pixel = None
        self.clicked_y_pixel = None
        self.file_path = None
        self.pixmap = None
        self.tennis_balls = {}
        self.buttons_list = []
        self.image_points = None
        self.road_points = None
        self.unit = 1.5
        self.image_name = ""

    def add_buttons(self):
        for i in range(0, 5):
            for j in range(0, 5):
                hbox = QHBoxLayout()
                edit_btn = EditButton("Edit")
                edit_btn.set_row_column(i, j)
                edit_btn.clicked.connect(self.edit_ball_position)
                button = AssignButton(f"Row={i}, Col={j}")
                button.set_row_column(i, j)
                button.clicked.connect(self.set_ball_coord_position)
                hbox.addWidget(button)
                hbox.addWidget(edit_btn)
                self.vbox.addLayout(hbox)
        self.widget.setLayout(self.vbox)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

    def browse_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg, *.png)')
        if fname[0]:
            self.change_image_reset()
            self.file_path = fname[0]
            self.image_name = fname[0].split("/")[-1]
            self.pixmap = QPixmap(self.file_path)
            self.image_holder.setText("")
            self.update()

    def change_image_reset(self):
        self.image_points = None
        self.road_points = None
        self.tennis_balls = {}
        self.reset_buttons_list()
        self.reset_ball_pixel_positions()

    def reset_buttons_list(self):
        if self.buttons_list:
            for btn in self.buttons_list:
                btn.reset_button_status()
        self.buttons_list = []

    def resize_widgets(self):
        imgholder_height = self.image_holder.height()
        imgholder_width = self.image_holder.width()
        self.image_holder.resize(self.pixmap.width(), self.pixmap.height())
        img_height = self.pixmap.height()
        img_width = self.pixmap.width()
        height_diff = 0
        width_diff = 0
        if img_height > imgholder_height:
            height_diff = img_height - imgholder_height
        if img_width > imgholder_width:
            width_diff = img_width - imgholder_width
        self.resize(self.width() + width_diff, self.height() + height_diff)

    def get_ball_pixel_position(self, event):
        if self.image_name:
            self.clicked_x_pixel = event.pos().x()
            self.clicked_y_pixel = event.pos().y()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.file_path:
            self.resize_widgets()
            painter.drawPixmap(QRect(self.image_holder.x(), self.image_holder.y(),
                                     self.image_holder.width(), self.image_holder.height()), self.pixmap)

        if self.clicked_x_pixel and self.clicked_y_pixel:
            pen = QPen(Qt.green, 3)
            painter.setPen(pen)
            self.draw_marker(painter, self.clicked_x_pixel+self.image_holder.x(),
                             self.clicked_y_pixel+self.image_holder.y())

        if self.tennis_balls:
            pen = QPen(Qt.green, 3)
            painter.setPen(pen)
            for ball in self.tennis_balls:
                x = self.tennis_balls[ball].x
                y = self.tennis_balls[ball].y
                self.draw_marker(painter, x+self.image_holder.x(), y+self.image_holder.y())

    @staticmethod
    def draw_marker(painter, x, y):
        painter.drawLine(x-10, y, x+10, y)
        painter.drawLine(x, y-10, x, y+10)

    def set_ball_coord_position(self):
        if self.clicked_y_pixel and self.clicked_x_pixel:
            button = self.sender()
            self.buttons_list.append(button)
            row, column = button.get_row_column()

            tennis_ball = TennisBall(x=self.clicked_x_pixel, y=self.clicked_y_pixel, r=row, c=column)
            self.tennis_balls[(row, column)] = tennis_ball
            tennis_ball.to_string()
            button.set_button_selected_status()
            self.reset_ball_pixel_positions()
            self.update()

    def reset_ball_pixel_positions(self):
        self.clicked_x_pixel = None
        self.clicked_y_pixel = None

    def save_balls(self):
        if len(self.tennis_balls) != 0:
            road_points = []
            image_points = []
            with open(f'output_csv/{self.image_name}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'row', 'column'])
                for ball in self.tennis_balls:
                    x = self.tennis_balls[ball].x
                    y = self.tennis_balls[ball].y
                    c = self.tennis_balls[ball].c * self.unit
                    r = self.tennis_balls[ball].r * self.unit
                    writer.writerow([x, y, c, r])
                    road_points.append([c, r])
                    image_points.append([x, y])

                csvfile.close()
            print("saved")
            self.image_points = np.array([image_points])
            self.road_points = np.array([road_points])

    def edit_ball_position(self):
        if self.tennis_balls:
            button = self.sender()
            r, c = button.get_row_column()
            if (r, c) in self.tennis_balls.keys():
                x, y = self.tennis_balls[(r, c)].x, self.tennis_balls[(r, c)].y
                self.edit_dialog.set_ball_position(x, y, r, c)
                self.edit_dialog.show()
                self.edit_dialog.exec_()
                n_x, n_y = self.edit_dialog.get_x_y()
                self.tennis_balls[(r, c)].set_x_y(n_x, n_y)
            else:
                print("key not found")
                return

    def calculate_homography(self):
        if self.road_points is not None and self.image_points is not None:
            print("calculate_homography")
            print(self.road_points)
            print(self.image_points)


def main():
    app = QApplication()
    window = LabelTennisBallGUI()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
