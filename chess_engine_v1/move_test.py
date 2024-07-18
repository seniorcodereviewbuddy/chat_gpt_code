import unittest

from move import Move
from square import Square


class TestMove(unittest.TestCase):
    def test_move_initialization(self):
        start = Square("e2")
        end = Square("e4")
        move = Move(start, end, "P", "p")
        self.assertEqual(move.start, start)
        self.assertEqual(move.end, end)
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, "p")
        self.assertIsNone(move.promotion_piece)

    def test_move_initialization_with_promotion(self):
        start = Square("e7")
        end = Square("e8")
        move = Move(start, end, "P", " ", "Q")
        self.assertEqual(move.start, start)
        self.assertEqual(move.end, end)
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, " ")
        self.assertEqual(move.promotion_piece, "Q")

    def test_move_str(self):
        start = Square("e2")
        end = Square("e4")
        move = Move(start, end, "P", "p")
        self.assertEqual(str(move), "P from e2 to e4, capturing p")

    def test_move_str_with_promotion(self):
        start = Square("e7")
        end = Square("e8")
        move = Move(start, end, "P", " ", "Q")
        self.assertEqual(str(move), "P from e7 to e8, capturing  , promoting to Q")

    def test_move_repr(self):
        start = Square("e2")
        end = Square("e4")
        move = Move(start, end, "P", "p")
        self.assertEqual(repr(move), "P from e2 to e4, capturing p")

    def test_move_repr_with_promotion(self):
        start = Square("e7")
        end = Square("e8")
        move = Move(start, end, "P", " ", "Q")
        self.assertEqual(repr(move), "P from e7 to e8, capturing  , promoting to Q")

    def test_move_equality(self):
        start1 = Square("e2")
        end1 = Square("e4")
        move1 = Move(start1, end1, "P", "p")
        start2 = Square("e2")
        end2 = Square("e4")
        move2 = Move(start2, end2, "P", "p")
        self.assertEqual(move1, move2)

    def test_move_inequality(self):
        start1 = Square("e2")
        end1 = Square("e4")
        move1 = Move(start1, end1, "P", "p")
        start2 = Square("d2")
        end2 = Square("d4")
        move2 = Move(start2, end2, "P", "p")
        self.assertNotEqual(move1, move2)

    def test_move_inequality_with_promotion(self):
        start1 = Square("e7")
        end1 = Square("e8")
        move1 = Move(start1, end1, "P", " ", "Q")
        start2 = Square("e7")
        end2 = Square("e8")
        move2 = Move(start2, end2, "P", " ", "R")
        self.assertNotEqual(move1, move2)

    def test_move_hash(self):
        start1 = Square("e2")
        end1 = Square("e4")
        move1 = Move(start1, end1, "P", "p")
        start2 = Square("e2")
        end2 = Square("e4")
        move2 = Move(start2, end2, "P", "p")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)

    def test_move_hash_with_promotion(self):
        start1 = Square("e7")
        end1 = Square("e8")
        move1 = Move(start1, end1, "P", " ", "Q")
        start2 = Square("e7")
        end2 = Square("e8")
        move2 = Move(start2, end2, "P", " ", "Q")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)


if __name__ == "__main__":
    unittest.main()
