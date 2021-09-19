import random


class RubiksCube:
    WHITE = 'W'
    GREEN = 'G'
    RED = 'R'
    BLUE = 'B'
    ORANGE = 'O'
    YELLOW = 'Y'
    CUBE_FACES = [WHITE, GREEN, RED, BLUE, ORANGE, YELLOW]
    PIECE_FACES_PER_SIDE = 9

    def __init__(self):
        self.faces = []
        for face in self.CUBE_FACES:
            for i in range(self.PIECE_FACES_PER_SIDE):
                self.faces += face
        print("Rubik's Cube Initialized with colors: {}".format(self.asString()))

    def asString(self):
        string = ""
        index = 0
        for face in self.faces:
            string += face
            index += 1
            if index % 9 == 0:
                string += ' '
        return string

    def shuffle(self, move_count):
        print("Shuffling Cube")
        for i in range(move_count):
            rand = random.randint(1, 12)
            if rand == 1:
                self.rotateWhite()
            elif rand == 2:
                self.rotateWhite(cc=True)
            elif rand == 3:
                self.rotateGreen()
            elif rand == 4:
                self.rotateGreen(cc=True)
            elif rand == 5:
                self.rotateRed()
            elif rand == 6:
                self.rotateRed(cc=True)
            elif rand == 7:
                self.rotateBlue()
            elif rand == 8:
                self.rotateBlue(cc=True)
            elif rand == 9:
                self.rotateOrange()
            elif rand == 10:
                self.rotateOrange(cc=True)
            elif rand == 11:
                self.rotateYellow()
            elif rand == 12:
                self.rotateYellow(cc=True)

    def rotateWhite(self, cc=False):
        rotation = "counterclockwise (U')" if cc else "clockwise (U)"
        print("Rotating white face {}".format(rotation))
        # FACE:
        self._swap(1, 5, 7, 3, cc)
        self._swap(0, 2, 8, 6, cc)
        # BORDER:
        self._swap(9, 36, 27, 18, cc)
        self._swap(10, 37, 28, 19, cc)
        self._swap(11, 38, 29, 20, cc)
        print("New Orientation: {}".format(self.asString()))

    def rotateGreen(self, cc=False):
        rotation = "counterclockwise (F')" if cc else "clockwise (F)"
        print("Rotating green face {}".format(rotation))
        # FACE:
        self._swap(10, 14, 16, 12, cc)
        self._swap(9, 11, 17, 15, cc)
        # BORDER:
        self._swap(8, 24, 47, 38, cc)
        self._swap(7, 21, 50, 41, cc)
        self._swap(6, 18, 53, 44, cc)
        print("New Orientation: {}".format(self.asString()))

    def rotateRed(self, cc=False):
        rotation = "counterclockwise (R')" if cc else "clockwise (R)"
        print("Rotating red face {}".format(rotation))
        # FACE:
        self._swap(19, 23, 25, 21, cc)
        self._swap(18, 20, 26, 24, cc)
        # BORDER:
        self._swap(2, 33, 53, 11, cc)
        self._swap(5, 30, 52, 14, cc)
        self._swap(8, 27, 51, 17, cc)
        print("New Orientation: {}".format(self.asString()))

    def rotateBlue(self, cc=False):
        rotation = "counterclockwise (B')" if cc else "clockwise (B)"
        print("Rotating blue face {}".format(rotation))
        # FACE:
        self._swap(28, 32, 34, 30, cc)
        self._swap(27, 29, 35, 33, cc)
        # BORDER:
        self._swap(0, 42, 51, 20, cc)
        self._swap(1, 39, 48, 23, cc)
        self._swap(2, 36, 45, 26, cc)
        print("New Orientation: {}".format(self.asString()))

    def rotateOrange(self, cc=False):
        rotation = "counterclockwise (L')" if cc else "clockwise (L)"
        print("Rotating orange face {}".format(rotation))
        # FACE:
        self._swap(37, 41, 43, 39, cc)
        self._swap(36, 38, 44, 42, cc)
        # BORDER:
        self._swap(6, 15, 45, 29, cc)
        self._swap(3, 12, 46, 32, cc)
        self._swap(0, 9, 47, 35, cc)
        print("New Orientation: {}".format(self.asString()))

    def rotateYellow(self, cc=False):
        rotation = "counterclockwise (D')" if cc else "clockwise (D)"
        print("Rotating yellow face {}".format(rotation))
        # FACE:
        self._swap(46, 50, 52, 48, cc)
        self._swap(45, 47, 53, 51, cc)
        # BORDER:
        self._swap(17, 26, 35, 44, cc)
        self._swap(16, 25, 34, 43, cc)
        self._swap(15, 24, 33, 42, cc)
        print("New Orientation: {}".format(self.asString()))

    def _swap(self, index_1, index_2, index_3, index_4, cc=False):
        if cc:
            temp = self.faces[index_1]
            self.faces[index_1] = self.faces[index_2]
            self.faces[index_2] = self.faces[index_3]
            self.faces[index_3] = self.faces[index_4]
            self.faces[index_4] = temp
        else:
            temp = self.faces[index_1]
            self.faces[index_1] = self.faces[index_4]
            self.faces[index_4] = self.faces[index_3]
            self.faces[index_3] = self.faces[index_2]
            self.faces[index_2] = temp
