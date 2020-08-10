class TennisBall:
    def __init__(self, x=None, y=None, r=None, c=None):
        self.x = x
        self.y = y
        self.r = r
        self.c = c

    def set_x_y(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        print(f"row={self.r}, column={self.c}, x={self.x}, y={self.y}")
