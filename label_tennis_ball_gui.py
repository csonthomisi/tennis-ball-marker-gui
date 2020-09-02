from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

from assign_button import AssignButton
from edit_button import EditButton
from edit_position_gui import EditPositionGUI
from photo_viewer import PhotoViewer
from region_growing import RegionGrowing
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

        self.viewer = PhotoViewer(self)
        self.btn_pix_info = QtWidgets.QToolButton(self)
        self.btn_pix_info.setText('Enter pixel info mode')
        self.btn_pix_info.clicked.connect(self.pix_info)
        self.edit_pix_info = QtWidgets.QLineEdit(self)
        self.edit_pix_info.setReadOnly(True)
        self.viewer.photoClicked.connect(self.get_ball_pixel_position)
        self.image_holder.addWidget(self.viewer)
        hblayout = QtWidgets.QHBoxLayout()
        hblayout.setAlignment(Qt.AlignLeft)
        hblayout.addWidget(self.btn_pix_info)
        hblayout.addWidget(self.edit_pix_info)
        self.image_holder.addLayout(hblayout)

        self.clicked_x_pixel = None
        self.clicked_y_pixel = None
        self.temp_x_pixel = None
        self.temp_y_pixel = None
        self.file_path = None
        self.pixmap = None
        self.tennis_balls = {}
        self.buttons_list = []
        self.image_points = None
        self.road_points = None
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
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'c\\')
        if fname[0]:
            self.change_image_reset()
            self.file_path = fname[0]
            self.image_name = fname[0].split("/")[-1]
            self.load_image()

    def change_image_reset(self):
        self.image_points = None
        self.road_points = None
        self.delete_markers()
        self.tennis_balls = {}
        self.reset_buttons_list()
        self.reset_ball_pixel_positions()

    def load_image(self):
        self.viewer.setPhoto(QPixmap(self.file_path))

    def pix_info(self):
        self.viewer.toggleDragMode()

    def get_ball_pixel_position(self, event):
        if self.viewer.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            if self.image_name:
                self.clicked_x_pixel = event.x()
                self.clicked_y_pixel = event.y()
                self.estimate_center()

    def estimate_center(self):
        img = RegionGrowing(img_path=self.file_path, row=self.clicked_y_pixel, col=self.clicked_x_pixel, thresh=5)
        img.region_grow()
        self.clicked_x_pixel, self.clicked_y_pixel = img.estimate_center()
        self.edit_pix_info.setText(f"Estimated center: {self.clicked_x_pixel}, {self.clicked_y_pixel}")
        if self.temp_x_pixel and self.temp_y_pixel:
            self.viewer.remove_marker(self.temp_x_pixel, self.temp_y_pixel)
        self.viewer.add_marker(self.clicked_x_pixel, self.clicked_y_pixel)
        self.temp_x_pixel, self.temp_y_pixel = self.clicked_x_pixel, self.clicked_y_pixel

    def set_ball_coord_position(self):
        if self.clicked_y_pixel and self.clicked_x_pixel:
            button = self.sender()
            row, column = button.get_row_column()
            if not (row, column) in self.tennis_balls:
                self.buttons_list.append(button)
                tennis_ball = TennisBall(x=self.clicked_x_pixel, y=self.clicked_y_pixel, r=row, c=column)
                self.tennis_balls[(row, column)] = tennis_ball
                tennis_ball.to_string()
                button.set_button_selected_status()
                self.reset_ball_pixel_positions()

    def reset_buttons_list(self):
        if self.buttons_list:
            for btn in self.buttons_list:
                btn.reset_button_status()
        self.buttons_list = []

    def reset_ball_pixel_positions(self):
        self.clicked_x_pixel, self.clicked_y_pixel = None, None
        self.temp_x_pixel, self.temp_y_pixel = None, None

    def delete_markers(self):
        if self.tennis_balls:
            for key in self.tennis_balls:
                self.viewer.remove_marker(self.tennis_balls[key].x, self.tennis_balls[key].y)

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
                    c = self.tennis_balls[ball].c * self.road_unit.value()
                    r = self.tennis_balls[ball].r * self.road_unit.value()
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
                p_x, p_y = self.edit_dialog.get_prev_x_y()
                self.viewer.remove_marker(p_x, p_y)
                self.viewer.add_marker(n_x, n_y)
                self.tennis_balls[(r, c)].set_x_y(n_x, n_y)
            else:
                print("key not found")
                return

    def calculate_homography(self):
        self.save_balls()
        if self.road_points is not None and self.image_points is not None:
            if self.imu.isChecked():
                print("IMU calculate_homography")
                print(self.road_points)
                print(self.image_points)
            elif self.utm.isChecked():
                print("UTM calculate_homography")
                print(self.road_points)
                print(self.image_points)
            else:
                pass


def main():
    app = QApplication()
    window = LabelTennisBallGUI()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
