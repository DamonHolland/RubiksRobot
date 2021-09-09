class Piece:
    def __init__(self, top_color, bottom_color, left_color, right_color, front_color, back_color):
        self.colors = [left_color, right_color, bottom_color, top_color, front_color, back_color]

    def rotate_C(self):
        temp = self.colors[5]
        self.colors[5] = self.colors[0]
        self.colors[0] = self.colors[4]
        self.colors[4] = self.colors[1]
        self.colors[1] = temp
