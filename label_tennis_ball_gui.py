from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

from ui_components.assign_button import AssignButton
from ui_components.delete_button import DeleteButton
from ui_components.edit_button import EditButton
from ui_components.edit_position_gui import EditPositionGUI
from ui_components.photo_viewer import PhotoViewer
from region_growing.region_growing import RegionGrowing
from components.tennis_ball import TennisBall
from ui.gui import Ui_MainWindow
import csv
import numpy as np
import pandas as pd


class LabelTennisBallGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.edit_dialog = EditPositionGUI()
        self.buttons_list = {}
        self.add_buttons()
        self.select_image_btn.clicked.connect(self.browse_image)
        self.calc_homography_btn.clicked.connect(self.calculate_homography)
        self.load_btn.clicked.connect(self.load_coordinates)

        self.viewer = PhotoViewer(self)
        self.btn_pix_info = QtWidgets.QToolButton(self)
        self.btn_pix_info.setText('Enter pixel info mode')
        self.btn_pix_info.clicked.connect(self.pix_info)
        self.edit_pix_info = QtWidgets.QLineEdit(self)
        self.edit_pix_info.setReadOnly(True)
        self.viewer.photoClicked.connect(self.on_image_click)
        self.image_holder.addWidget(self.viewer)
        hblayout = QtWidgets.QHBoxLayout()
        hblayout.setAlignment(Qt.AlignLeft)
        hblayout.addWidget(self.btn_pix_info)
        hblayout.addWidget(self.edit_pix_info)
        self.image_holder.addLayout(hblayout)

        self.clicked_x_pixel = None
        self.clicked_y_pixel = None
        self.file_path = None
        self.pixmap = None
        self.tennis_balls = {}
        self.image_points = None
        self.road_points = None
        self.image_name = ""

    def add_buttons(self):
        for i in range(0, 5):
            for j in range(0, 5):
                hbox = QHBoxLayout()
                edit_btn = EditButton()
                edit_btn.set_row_column(i, j)
                edit_btn.clicked.connect(self.edit_ball_position)
                button = AssignButton(f"Row={i}, Col={j}")
                button.set_row_column(i, j)
                button.clicked.connect(self.match_pixel_road_points)
                self.buttons_list[(i, j)] = button
                delete_button = DeleteButton()
                delete_button.set_row_column(i, j)
                delete_button.clicked.connect(self.unmatch_pixel_road_points)
                hbox.addWidget(button)
                hbox.addWidget(edit_btn)
                hbox.addWidget(delete_button)
                self.vbox.addLayout(hbox)
        self.widget.setLayout(self.vbox)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

    def browse_image(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', 'c\\')
        if file_name[0]:
            self.image_change_reset()
            self.file_path = file_name[0]
            self.image_name = file_name[0].split("/")[-1]
            self.load_image()

    def image_change_reset(self):
        self.image_points = None
        self.road_points = None
        self.clear_markers()
        self.tennis_balls = {}
        self.reset_buttons_list()
        self.reset_ball_pixel_positions()

    def load_image(self):
        self.viewer.setPhoto(QPixmap(self.file_path))

    def pix_info(self):
        self.viewer.toggleDragMode()

    def on_image_click(self, event):
        if self.viewer.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            if self.image_name:
                x, y = self.estimate_center(event.x(), event.y())
                self.remove_temp_marker()
                self.add_marker(x, y)
                self.save_estimated_coordinates(x, y)

    def estimate_center(self, x, y):
        img = RegionGrowing(img_path=self.file_path, row=y, col=x, thresh=5)
        img.region_grow()
        estimated_x, estimated_y = img.estimate_center()
        self.edit_pix_info.setText(f"Estimated center: {estimated_x}, {estimated_y}")
        return estimated_x, estimated_y

    def remove_temp_marker(self):
        if self.clicked_x_pixel and self.clicked_y_pixel:
            self.delete_marker(self.clicked_x_pixel, self.clicked_y_pixel)

    def delete_marker(self, x, y):
        self.viewer.remove_marker(x, y)

    def add_marker(self, x, y):
        self.viewer.add_marker(x, y)

    def save_estimated_coordinates(self, x, y):
        self.clicked_x_pixel = x
        self.clicked_y_pixel = y

    def match_pixel_road_points(self):
        if self.clicked_y_pixel and self.clicked_x_pixel:
            button = self.sender()
            row, column = button.get_row_column()
            if not (row, column) in self.tennis_balls:
                self.add_tennis_ball(self.clicked_x_pixel, self.clicked_y_pixel, row, column)
                button.set_button_status_selected()
                self.reset_ball_pixel_positions()

    def reset_buttons_list(self):
        for key in self.buttons_list:
            btn = self.buttons_list[key]
            if btn.is_selected():
                btn.set_button_status_default()

    def reset_ball_pixel_positions(self):
        self.clicked_x_pixel = None
        self.clicked_y_pixel = None

    def clear_markers(self):
        self.delete_markers()
        self.remove_temp_marker()

    def delete_markers(self):
        if self.tennis_balls:
            for key in self.tennis_balls:
                self.delete_marker(self.tennis_balls[key].x, self.tennis_balls[key].y)

    def unmatch_pixel_road_points(self):
        if self.tennis_balls:
            button = self.sender()
            r, c = button.get_row_column()
            if (r, c) in self.tennis_balls.keys():
                x, y = self.tennis_balls[(r, c)].x, self.tennis_balls[(r, c)].y
                self.delete_marker(x, y)
                btn = self.get_button(r, c)
                btn.set_button_status_default()
                del self.tennis_balls[(r, c)]

    def edit_ball_position(self):
        if self.tennis_balls:
            button = self.sender()
            r, c = button.get_row_column()
            if (r, c) in self.tennis_balls.keys():
                x, y = self.tennis_balls[(r, c)].x, self.tennis_balls[(r, c)].y
                self.open_edit_dialog(x, y, r, c)
                n_x, n_y = self.edit_dialog.get_x_y()
                self.delete_marker(x, y)
                self.add_marker(n_x, n_y)
                self.tennis_balls[(r, c)].set_x_y(n_x, n_y)
            else:
                self.edit_pix_info.setText("Button doesn't have pixel value")
                return

    def open_edit_dialog(self, x, y, r, c):
        self.edit_dialog.set_ball_position(x, y, r, c)
        self.edit_dialog.show()
        self.edit_dialog.exec_()

    def load_coordinates(self):
        if self.file_path:
            file_name = QFileDialog.getOpenFileName(self, 'Open File', 'c\\')
            if file_name[0]:
                x_arr, y_arr, r_arr, c_arr, u_arr = self.get_data_from_file(file_name[0])
                self.road_unit.setValue(u_arr[0])
                for i in range(len(x_arr)):
                    self.add_marker(x_arr[i], y_arr[i])
                    btn = self.get_button(r_arr[i], c_arr[i])
                    btn.set_button_status_selected()
                    self.add_tennis_ball(x_arr[i], y_arr[i], r_arr[i], c_arr[i])

    @staticmethod
    def get_data_from_file(file):
        data = pd.read_csv(file)
        x = np.array(data['x'])
        y = np.array(data['y'])
        r = np.array(data['row'])
        c = np.array(data['column'])
        u = np.array(data['unit'])
        return x, y, r, c, u

    def get_button(self, r, c):
        if (r, c) in self.buttons_list.keys():
            return self.buttons_list[(r, c)]

    def add_tennis_ball(self, x, y, r, c):
        tb = TennisBall(x=x, y=y, r=r, c=c)
        self.tennis_balls[(r, c)] = tb
        self.edit_pix_info.setText(tb.to_string())

    def calculate_homography(self):
        self.save_balls()
        if self.road_points is not None and self.image_points is not None:
            if self.imu.isChecked():
                self.edit_pix_info.setText("IMU calculate_homography")
                print(self.road_points)
                print(self.image_points)
            elif self.utm.isChecked():
                self.edit_pix_info.setText("UTM calculate_homography")
                print(self.road_points)
                print(self.image_points)
            else:
                pass

    def save_balls(self):
        if len(self.tennis_balls) != 0:
            road_points = []
            image_points = []
            u = self.road_unit.value()
            with open(f'output_csv/{self.image_name}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'row', 'column', 'unit'])
                for ball in self.tennis_balls:
                    x = self.tennis_balls[ball].x
                    y = self.tennis_balls[ball].y
                    r = self.tennis_balls[ball].r
                    c = self.tennis_balls[ball].c
                    writer.writerow([x, y, r, c, u])
                    road_points.append([self.tennis_balls[ball].c * self.road_unit.value(),
                                        self.tennis_balls[ball].r * self.road_unit.value()])
                    image_points.append([x, y])
                csvfile.close()
            self.edit_pix_info.setText(f"Saved to output_csv/{self.image_name}.csv")
            self.image_points = np.array([image_points])
            self.road_points = np.array([road_points])


def main():
    app = QApplication()
    window = LabelTennisBallGUI()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
