import unittest
from chess_engine import Board, ChessEngine, Pieces

# TODO: Chris: Fix all tests.

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

    # TODO: ChatGPT: Add non-new game FEN tests.

    # TODO: ChatGPT: Add tests for:
    # -Different positions
    # -Black pieces
    # -En-passant pawn captures
    # -Pawn promotions
    # -Where some squares are blocked

    def test_generate_pawn_moves(self):
        # Test pawn move generation
        self.board.board[6][0] = Pieces.WHITE_PAWN
        moves = self.board.generate_piece_moves(6, 0)
        expected_moves = [((6, 0), (5, 0)), ((6, 0), (4, 0))]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_rook_moves(self):
        # Test rook move generation
        self.board.board[4][4] = Pieces.WHITE_ROOK
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (4, 5)), ((4, 4), (4, 6)), ((4, 4), (4, 7)),
            ((4, 4), (4, 3)), ((4, 4), (4, 2)), ((4, 4), (4, 1)), ((4, 4), (4, 0)),
            ((4, 4), (5, 4)), ((4, 4), (6, 4)), ((4, 4), (7, 4)),
            ((4, 4), (3, 4)), ((4, 4), (2, 4)), ((4, 4), (1, 4)), ((4, 4), (0, 4)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_knight_moves(self):
        # Test knight move generation
        self.board.board[4][4] = Pieces.WHITE_KNIGHT
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (6, 5)), ((4, 4), (6, 3)), ((4, 4), (5, 6)), ((4, 4), (5, 2)),
            ((4, 4), (3, 6)), ((4, 4), (3, 2)), ((4, 4), (2, 5)), ((4, 4), (2, 3)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_bishop_moves(self):
        # Test bishop move generation
        self.board.board[4][4] = Pieces.WHITE_BISHOP
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (5, 5)), ((4, 4), (6, 6)), ((4, 4), (7, 7)),
            ((4, 4), (3, 3)), ((4, 4), (2, 2)), ((4, 4), (1, 1)), ((4, 4), (0, 0)),
            ((4, 4), (5, 3)), ((4, 4), (6, 2)), ((4, 4), (7, 1)),
            ((4, 4), (3, 5)), ((4, 4), (2, 6)), ((4, 4), (1, 7)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_queen_moves(self):
        # Test queen move generation
        self.board.board[4][4] = Pieces.WHITE_QUEEN
        moves = self.board.generate_piece_moves(4, 4)
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
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_king_moves(self):
        # Test king move generation
        self.board.board[4][4] = Pieces.WHITE_KING
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (5, 4)), ((4, 4), (5, 5)), ((4, 4), (4, 5)),
            ((4, 4), (3, 5)), ((4, 4), (3, 4)), ((4, 4), (3, 3)),
            ((4, 4), (4, 3)), ((4, 4), (5, 3)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    # TODO: ChatGPT: Add more test cases here.
    # Tests should include ensuring undo returns captured pieces correctly.
    def test_make_and_undo_move(self):
        # Test making and undoing a move
        move = ((6, 0), (4, 0))
        self.board.make_move(move)
        self.assertEqual(self.board.board[6][0], '.')
        self.assertEqual(self.board.board[4][0], Pieces.WHITE_PAWN)
        self.board.undo_move(move, '.')
        self.assertEqual(self.board.board[6][0], Pieces.WHITE_PAWN)
        self.assertEqual(self.board.board[4][0], '.')

    def test_evaluate(self):
        # Test the evaluation function
        self.assertEqual(self.engine.evaluate(), 0)  # Initial position is balanced

        # Test a board with a material imbalance
        self.board.board[4][4] = 'Q'  # Add a white queen in the center
        self.assertEqual(self.engine.evaluate(), 9)

    def test_best_move(self):
        # White has 2 pawn that can't move and a king in the corner that can only move to one square.
        # So there is only one move white can make.
        fen = '8/8/8/8/7k/6pp/6PP/7K w - - 0 1'
        board = Board(self.fen)
        engine = ChessEngine(self.board)

        # Test the best move function
        move = self.engine.best_move(1)
        # TODO: Chris: Pretty sure this is wrong, but it's at least constant.
        self.assertEqual(move, ((7, 3), (1, 3)))
        

if __name__ == "__main__":
    unittest.main()
