import unittest

from square import Square, Squares


class TestSquare(unittest.TestCase):
    def test_square_initialization(self):
        square = Square("e4")
        self.assertEqual(square.algebraic, "e4")
        self.assertEqual(square.row, 3)
        self.assertEqual(square.col, 4)

    def test_square_row(self):
        self.assertEqual(Squares.A1.row, 0)
        self.assertEqual(Squares.B8.row, 7)
        self.assertEqual(Squares.C2.row, 1)
        self.assertEqual(Squares.D7.row, 6)
        self.assertEqual(Squares.E3.row, 2)
        self.assertEqual(Squares.F6.row, 5)
        self.assertEqual(Squares.G4.row, 3)
        self.assertEqual(Squares.H5.row, 4)

    def test_square_col(self):
        self.assertEqual(Squares.A1.col, 0)
        self.assertEqual(Squares.B8.col, 1)
        self.assertEqual(Squares.C2.col, 2)
        self.assertEqual(Squares.D7.col, 3)
        self.assertEqual(Squares.E3.col, 4)
        self.assertEqual(Squares.F6.col, 5)
        self.assertEqual(Squares.G4.col, 6)
        self.assertEqual(Squares.H5.col, 7)

    def test_square_str(self):
        square = Square("e4")
        self.assertEqual(str(square), "e4")

    def test_square_repr(self):
        square = Square("e4")
        self.assertEqual(repr(square), "e4")

    def test_square_equality(self):
        square1 = Square("e4")
        square2 = Square("e4")
        self.assertEqual(square1, square2)

    def test_square_inequality(self):
        square1 = Square("e4")
        square2 = Square("d4")
        self.assertNotEqual(square1, square2)

    def test_square_hash(self):
        square1 = Square("e4")
        square2 = Square("e4")
        square_set = {square1, square2}
        self.assertEqual(len(square_set), 1)

    def test_square_from_row_col(self):
        self.assertEqual(Squares.square_from_row_col(0, 0), Squares.A1)
        self.assertEqual(Squares.square_from_row_col(7, 7), Squares.H8)
        self.assertEqual(Squares.square_from_row_col(4, 4), Squares.E5)
        self.assertEqual(Squares.square_from_row_col(6, 2), Squares.C7)
        self.assertEqual(Squares.square_from_row_col(2, 6), Squares.G3)


if __name__ == "__main__":
    unittest.main()
