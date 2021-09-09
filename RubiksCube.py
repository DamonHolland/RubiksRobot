import Colors
import Piece


class RubiksCube:
    pieces = [Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.WHITE, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.GREEN, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLUE, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.ORANGE),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.GREEN, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLUE, Colors.BLACK, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.GREEN, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLACK, Colors.RED, Colors.BLACK),
              Piece.Piece(Colors.BLACK, Colors.YELLOW, Colors.BLACK, Colors.BLUE, Colors.RED, Colors.BLACK)]

    def U(self):
        # Swap Corners
        temp = self.pieces[0]
        self.pieces[0] = self.pieces[6]
        self.pieces[6] = self.pieces[8]
        self.pieces[8] = self.pieces[2]
        self.pieces[2] = temp
        # Swap Edges
        temp = self.pieces[1]
        self.pieces[1] = self.pieces[3]
        self.pieces[3] = self.pieces[7]
        self.pieces[7] = self.pieces[5]
        self.pieces[5] = temp
        # Rotate Piece Faces
        self.pieces[0].rotate_C()
        self.pieces[1].rotate_C()
        self.pieces[2].rotate_C()
        self.pieces[3].rotate_C()
        self.pieces[5].rotate_C()
        self.pieces[6].rotate_C()
        self.pieces[7].rotate_C()
        self.pieces[8].rotate_C()
