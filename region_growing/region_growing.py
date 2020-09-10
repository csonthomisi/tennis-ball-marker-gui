import numpy as np
import cv2
from components.point import Point


class RegionGrowing:
    def __init__(self, img_path, row, col, thresh=5):
        self.img = cv2.imread(img_path, 0)
        self.seeds = [Point(row, col)]
        self.thresh = thresh
        self.seed_mark = np.zeros(self.img.shape)
        self.max_x, self.min_x = row, row
        self.max_y, self.min_y = col, col

    def get_gray_diff(self, current_point, tmp_point):
        return abs(int(self.img[current_point.x, current_point.y]) - int(self.img[tmp_point.x, tmp_point.y]))

    @staticmethod
    def select_connects(p):
        if p != 0:
            connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1),
                        Point(-1, 0)]
        else:
            connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
        return connects

    def region_grow(self, p=1):
        height, weight = self.img.shape
        seed_list = []
        for seed in self.seeds:
            seed_list.append(seed)
        label = 1
        connects = self.select_connects(p)
        while len(seed_list) > 0:
            current_point = seed_list.pop(0)

            self.seed_mark[current_point.x, current_point.y] = label

            for i in range(8):
                tmp_x = current_point.x + connects[i].x
                tmp_y = current_point.y + connects[i].y
                if tmp_x < 0 or tmp_y < 0 or tmp_x >= height or tmp_y >= weight:
                    continue
                if tmp_x > self.max_x:
                    self.max_x = tmp_x
                if tmp_x < self.min_x:
                    self.min_x = tmp_x
                if tmp_y > self.max_y:
                    self.max_y = tmp_y
                if tmp_y < self.min_y:
                    self.min_y = tmp_y
                gray_diff = self.get_gray_diff(current_point, Point(tmp_x, tmp_y))
                if gray_diff < self.thresh and self.seed_mark[tmp_x, tmp_y] == 0:
                    self.seed_mark[tmp_x, tmp_y] = label
                    seed_list.append(Point(tmp_x, tmp_y))
        self.min_x = self.min_x+1
        self.min_y = self.min_y+1
        self.max_x = self.max_x-1
        self.max_y = self.max_y-1

    def visualize_img(self):
        cv2.imshow(' ', self.seed_mark)
        cv2.waitKey(0)

    def visualize_region(self, margin=2):
        cv2.imshow(' ', self.seed_mark[self.min_x-margin:self.max_x+1+margin, self.min_y-margin:self.max_y+1+margin])
        cv2.waitKey(0)

    def get_boundaries(self):
        return self.min_x, self.min_y, self.max_x, self.max_y

    def get_result_img_array(self):
        return self.seed_mark

    def get_region_array(self):
        return self.seed_mark[self.min_x:self.max_x+1, self.min_y:self.max_y+1]

    def estimate_center(self):
        y_center = self.min_y + (self.max_y - self.min_y)/2
        x_center = self.max_x - 0.15*(self.max_x-self.min_x)
        return y_center, x_center
