from PySide2.QtCore import QRect
from PySide2.QtGui import QPixmap, Qt, QImage, QPainter, QBrush, QPen
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

from assign_button import AssignButton
from edit_button import EditButton
from edit_position_gui import EditPositionGUI
from tennis_ball import TennisBall
from ui.gui import Ui_MainWindow
import csv


class LabelTennisBallGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.img = None
        self.pixmap = None
        self.clicked_x_pixel = None
        self.clicked_y_pixel = None
        self.painter = QPainter(self)
        self.edit_dialog = EditPositionGUI()
        self.tennis_balls = {}
        self.add_buttons()
        self.select_image_btn.clicked.connect(self.browse_image)
        self.calc_homography_btn.clicked.connect(self.calculate_homography)
        self.save_btn.clicked.connect(self.save_balls)

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
        image_path = fname[0]
        self.img = QImage(image_path)
        pixmap = QPixmap(QPixmap.fromImage(self.img))
        self.image_holder.setPixmap(QPixmap(pixmap))
        self.resize_widgets()
        self.image_holder.mousePressEvent = self.get_ball_pixel_position

    def resize_widgets(self):
        self.image_holder.adjustSize()
        img_height = self.img.height()
        img_width = self.img.width()
        height_diff = 0
        width_diff = 0
        if img_height > 680:
            height_diff = img_height - 680
        if img_width > 850:
            width_diff = img_width - 850
        self.resize(self.width()+width_diff, self.height()+height_diff)

    def get_ball_pixel_position(self, event):
        self.clicked_x_pixel = event.pos().x()
        self.clicked_y_pixel = event.pos().y()
        self.update()

    def set_ball_coord_position(self):
        button = self.sender()
        row, column = button.get_row_column()
        if self.clicked_y_pixel and self.clicked_x_pixel:
            tennis_ball = TennisBall(x=self.clicked_x_pixel, y=self.clicked_y_pixel, r=row, c=column)
            self.tennis_balls[(row, column)] = tennis_ball
            tennis_ball.to_string()
            button.set_button_selected_status()
            self.reset_ball_pixel_positions()

    def reset_ball_pixel_positions(self):
        self.clicked_x_pixel = None
        self.clicked_y_pixel = None

    def save_balls(self):
        if len(self.tennis_balls) != 0:
            with open('output.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['x', 'y', 'row', 'column'])
                for ball in self.tennis_balls:
                    writer.writerow([self.tennis_balls[ball].x, self.tennis_balls[ball].y,
                                     self.tennis_balls[ball].r, self.tennis_balls[ball].c])
                csvfile.close()
        print("saved")

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
        print("calculate_homography")


app = QApplication()
window = LabelTennisBallGUI()
window.show()
app.exec_()
