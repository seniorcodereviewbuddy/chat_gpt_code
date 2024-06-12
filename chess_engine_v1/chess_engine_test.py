import unittest
from chess_engine import Board, ChessEngine

class TestChessEngine(unittest.TestCase):

    def setUp(self):
        # Initialize the board and engine with a starting position
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = Board(self.fen)
        self.engine = ChessEngine(self.board)

    def test_parse_fen(self):
        # Test the FEN parsing
        expected_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.assertEqual(self.board.board, expected_board)

    def test_generate_pawn_moves(self):
        # Test pawn move generation
        moves = self.board.generate_piece_moves('P', 6, 0)
        expected_moves = [((6, 0), (5, 0)), ((6, 0), (4, 0))]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_generate_rook_moves(self):
        # Test rook move generation
        self.board.board[4][4] = 'R'
        moves = self.board.generate_piece_moves('R', 4, 4)
        expected_moves = [
            ((4, 4), (4, 5)), ((4, 4), (4, 6)), ((4, 4), (4, 7)),
            ((4, 4), (4, 3)), ((4, 4), (4, 2)), ((4, 4), (4, 1)), ((4, 4), (4, 0)),
            ((4, 4), (5, 4)), ((4, 4), (6, 4)), ((4, 4), (7, 4)),
            ((4, 4), (3, 4)), ((4, 4), (2, 4)), ((4, 4), (1, 4)), ((4, 4), (0, 4)),
        ]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_generate_knight_moves(self):
        # Test knight move generation
        self.board.board[4][4] = 'N'
        moves = self.board.generate_piece_moves('N', 4, 4)
        expected_moves = [
            ((4, 4), (6, 5)), ((4, 4), (6, 3)), ((4, 4), (5, 6)), ((4, 4), (5, 2)),
            ((4, 4), (3, 6)), ((4, 4), (3, 2)), ((4, 4), (2, 5)), ((4, 4), (2, 3)),
        ]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_generate_bishop_moves(self):
        # Test bishop move generation
        self.board.board[4][4] = 'B'
        moves = self.board.generate_piece_moves('B', 4, 4)
        expected_moves = [
            ((4, 4), (5, 5)), ((4, 4), (6, 6)), ((4, 4), (7, 7)),
            ((4, 4), (3, 3)), ((4, 4), (2, 2)), ((4, 4), (1, 1)), ((4, 4), (0, 0)),
            ((4, 4), (5, 3)), ((4, 4), (6, 2)), ((4, 4), (7, 1)),
            ((4, 4), (3, 5)), ((4, 4), (2, 6)), ((4, 4), (1, 7)),
        ]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_generate_queen_moves(self):
        # Test queen move generation
        self.board.board[4][4] = 'Q'
        moves = self.board.generate_piece_moves('Q', 4, 4)
        expected_moves = [
            # Rook-like moves
            ((4, 4), (4, 5)), ((4, 4), (4, 6)), ((4, 4), (4, 7)),
            ((4, 4), (4, 3)), ((4, 4), (4, 2)), ((4, 4), (4, 1)), ((4, 4), (4, 0)),
            ((4, 4), (5, 4)), ((4, 4), (6, 4)), ((4, 4), (7, 4)),
            ((4, 4), (3, 4)), ((4, 4), (2, 4)), ((4, 4), (1, 4)), ((4, 4), (0, 4)),
            # Bishop-like moves
            ((4, 4), (5, 5)), ((4, 4), (6, 6)), ((4, 4), (7, 7)),
            ((4, 4), (3, 3)), ((4, 4), (2, 2)), ((4, 4), (1, 1)), ((4, 4), (0, 0)),
            ((4, 4), (5, 3)), ((4, 4), (6, 2)), ((4, 4), (7, 1)),
            ((4, 4), (3, 5)), ((4, 4), (2, 6)), ((4, 4), (1, 7)),
        ]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_generate_king_moves(self):
        # Test king move generation
        self.board.board[4][4] = 'K'
        moves = self.board.generate_piece_moves('K', 4, 4)
        expected_moves = [
            ((4, 4), (5, 4)), ((4, 4), (5, 5)), ((4, 4), (4, 5)),
            ((4, 4), (3, 5)), ((4, 4), (3, 4)), ((4, 4), (3, 3)),
            ((4, 4), (4, 3)), ((4, 4), (5, 3)),
        ]
        self.assertEqual(len(moves), len(expected_moves))
        for move in expected_moves:
            self.assertIn(move, moves)

    def test_make_and_undo_move(self):
        # Test making and undoing a move
        move = ((6, 0), (4, 0))
        self.board.make_move(move)
        self.assertEqual(self.board.board[6][0], '.')
        self.assertEqual(self.board.board[4][0], 'P')
        self.board.undo_move(move, '.')
        self.assertEqual(self.board.board[6][0], 'P')
        self.assertEqual(self.board.board[4][0], '.')

    def test_evaluate(self):
        # Test the evaluation function
        self.assertEqual(self.board.evaluate(), 0)  # Initial position is balanced

        # Test a board with a material imbalance
        self.board.board[4][4] = 'Q'  # Add a white queen in the center
        self.assertEqual(self.board.evaluate(), 9)

    def test_alpha_beta(self):
        # Test the alpha_beta function
        # This is a basic test to ensure the function runs without error and returns a value
        score, move = self.engine.alpha_beta(2, -float('inf'), float('inf'), True)
        self.assertIsInstance(score, (int, float))
        self.assertIsInstance(move, tuple)


    def test_best_move(self):
        # Test the best move function
        move = self.engine.best_move(1)
        self.assertIsNotNone(move)
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], tuple)
        self.assertIsInstance(move[1], tuple)
        self.assertEqual(len(move[0]), 2)
        self.assertEqual(len(move[1]), 2)

if __name__ == "__main__":
    unittest.main()
