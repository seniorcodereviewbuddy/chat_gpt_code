import unittest

from move import Move


class TestMove(unittest.TestCase):
    def test_move_initialization(self):
        move = Move((1, 0), (3, 0), "P", "p")
        self.assertEqual(move.start, (1, 0))
        self.assertEqual(move.end, (3, 0))
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, "p")
        self.assertIsNone(move.promotion_piece)

    def test_move_initialization_with_promotion(self):
        move = Move((6, 0), (7, 0), "P", " ", "Q")
        self.assertEqual(move.start, (6, 0))
        self.assertEqual(move.end, (7, 0))
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, " ")
        self.assertEqual(move.promotion_piece, "Q")

    def test_move_str(self):
        move = Move((1, 0), (3, 0), "P", "p")
        self.assertEqual(str(move), "P from (1, 0) to (3, 0), capturing p")

    def test_move_str_with_promotion(self):
        move = Move((6, 0), (7, 0), "P", " ", "Q")
        self.assertEqual(
            str(move), "P from (6, 0) to (7, 0), capturing  , promoting to Q"
        )

    def test_move_repr(self):
        move = Move((1, 0), (3, 0), "P", "p")
        self.assertEqual(repr(move), "P from (1, 0) to (3, 0), capturing p")

    def test_move_repr_with_promotion(self):
        move = Move((6, 0), (7, 0), "P", " ", "Q")
        self.assertEqual(
            repr(move), "P from (6, 0) to (7, 0), capturing  , promoting to Q"
        )

    def test_move_equality(self):
        move1 = Move((1, 0), (3, 0), "P", "p")
        move2 = Move((1, 0), (3, 0), "P", "p")
        self.assertEqual(move1, move2)

    def test_move_inequality(self):
        move1 = Move((1, 0), (3, 0), "P", "p")
        move2 = Move((1, 0), (2, 0), "P", "p")
        self.assertNotEqual(move1, move2)

    def test_move_inequality_with_promotion(self):
        move1 = Move((6, 0), (7, 0), "P", " ", "Q")
        move2 = Move((6, 0), (7, 0), "P", " ", "R")
        self.assertNotEqual(move1, move2)

    def test_move_hash(self):
        move1 = Move((1, 0), (3, 0), "P", "p")
        move2 = Move((1, 0), (3, 0), "P", "p")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)

    def test_move_hash_with_promotion(self):
        move1 = Move((6, 0), (7, 0), "P", " ", "Q")
        move2 = Move((6, 0), (7, 0), "P", " ", "Q")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)


if __name__ == "__main__":
    unittest.main()
