import enum

class Player(enum.Enum):
    WHITE = 1
    BLACK = 2

class Pieces(enum.StrEnum):
    WHITE_KING = 'K'
    WHITE_QUEEN = 'Q'
    WHITE_BISHOP = 'B'
    WHITE_KNIGHT = 'N'
    WHITE_ROOK = 'R'
    WHITE_PAWN = 'P'
    BLACK_KING = 'k'
    BLACK_QUEEN = 'q'
    BLACK_BISHOP = 'b'
    BLACK_KNIGHT = 'n'
    BLACK_ROOK = 'r'
    BLACK_PAWN = 'p'

BOARD_SIZE = 8

DIAGONAL_DIRECTIONS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
VERTICAL_AND_HORIZONTAL_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
ALL_DIRECTIONS = VERTICAL_AND_HORIZONTAL_DIRECTIONS + DIAGONAL_DIRECTIONS
KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

class FENRecord:
    # TODO: Add tests for FENRecord.

    """You can learn more about the FEN Record format at https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation"""
    def __init__(self, fen_str):
        fen_parts = fen_str.split(' ')
        self.board_str = fen_parts[0]

        # TODO: ChatGPT: Handle rest of FEN string.

    
    def board(self):
        def valid_board_character(character):
            return character in  ['k', 'K', 'Q', 'q', 'B', 'b', 'N', 'n', 'R', 'r', 'P', 'p']

        board = []
        rows = self.board_str.split('/')
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(['.'] * int(char))
                else:
                    if valid_board_character:
                        board_row.append(char)
                    else:
                        raise Exception(f"Invalid chracter in FEN board, {char}")

            if len(board_row) != BOARD_SIZE:
                raise Exception(f"FEN record error, found row of size {len(board_row)}, expecting {BOARD_SIZE}")
            board.append(board_row)
        return board

class Board:
    def __init__(self, fen_str):
        # Initialize the board using FEN notation
        fen = FENRecord(fen_str)
        self.board = fen.board()
        self.turn = Player.WHITE

    def display(self):
        # Print the board state
        for row in self.board:
            print(' '.join(row))
        print()

    def _piece_owned_by_current_player(self, piece):
        return piece.isupper() if self.turn == Player.WHITE else piece.islower()

    def _piece_capturable_by_current_player(self, piece):
        return not self._piece_owned_by_current_player(piece)

    def generate_moves(self):
        # Generate all legal moves for the current player
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if self._piece_owned_by_current_player(piece):
                    moves.extend(self.generate_piece_moves(r, c))
        return moves

    def generate_piece_moves(self, r, c):
        # Generate legal moves for a specific piece

        # TODO: ChatGPT: Remove moves that expose the king to capture.
        piece = self.board[r][c]
        if piece.upper() == Pieces.WHITE_PAWN:
            return self.generate_pawn_moves(r, c)
        elif piece.upper() == Pieces.WHITE_ROOK:
            return self.generate_rook_moves(r, c)
        elif piece.upper() == Pieces.WHITE_KNIGHT:
            return self.generate_knight_moves(r, c)
        elif piece.upper() == Pieces.WHITE_BISHOP:
            return self.generate_bishop_moves(r, c)
        elif piece.upper() == Pieces.WHITE_QUEEN:
            return self.generate_queen_moves(r, c)
        elif piece.upper() == Pieces.WHITE_KING:
            return self.generate_king_moves(r, c)

        raise Exception(f"Trying to generate moves for an unknown piece, {piece}")

    def generate_pawn_moves(self, r, c):
        # Generate legal pawn moves
        moves = []
        direction = -1 if self.turn == Player.WHITE else 1
        start_row = 6 if self.turn == Player.WHITE else 1

        # Single square move
        if self.board[r + direction][c] == '.':
            moves.append(((r, c), (r + direction, c)))
            # Double square move
            if r == start_row and self.board[r + 2 * direction][c] == '.':
                moves.append(((r, c), (r + 2 * direction, c)))

        # Captures
        # TODO: ChatGPT: Handle en-passant captures.
        for dc in [-1, 1]:
            new_r = r + direction
            new_c = c + dc
            if 0 <= new_c < BOARD_SIZE and self.board[new_r][new_c] != '.' and self._piece_capturable_by_current_player(self.board[new_r][new_c]):
                moves.append(((r, c), (new_r, new_c)))

        # TODO: ChatGPT: Handle promotion when the pawn reaches the final row.
        
        return moves

    def generate_rook_moves(self, r, c):
        # Generate legal rook moves
        return self.generate_sliding_moves(r, c, VERTICAL_AND_HORIZONTAL_DIRECTIONS)

    def generate_bishop_moves(self, r, c):
        # Generate legal bishop moves
        return self.generate_sliding_moves(r, c, DIAGONAL_DIRECTIONS)

    def generate_queen_moves(self, r, c):
        # Generate legal queen moves
        return self.generate_sliding_moves(r, c, ALL_DIRECTIONS)

    def _on_board(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def generate_sliding_moves(self, r, c, directions):
        # Generate sliding moves for rooks, bishops, and queens
        piece = self.board[r][c]
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self._on_board(nr, nc):
                if self.board[nr][nc] == '.':
                    moves.append(((r, c), (nr, nc)))
                elif self._piece_capturable_by_current_player(self.board[nr][nc]):
                     moves.append(((r, c), (nr, nc)))
                     break
                nr += dr
                nc += dc
        return moves

    def generate_knight_moves(self, r, c):
        # Generate legal knight moves
        moves = []
        for dr, dc in KNIGHT_MOVES:
            nr, nc = r + dr, c + dc
            if self._on_board(nr, nc):
                if self.board[nr][nc] == '.' or self._piece_capturable_by_current_player(self.board[nr][nc]):
                    moves.append(((r, c), (nr, nc)))
        return moves

    def generate_king_moves(self, r, c):
        # Generate legal king moves
        moves = []
        for dr, dc in ALL_DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self._on_board(nr, nc):
                if self.board[nr][nc] == '.' or self._piece_owned_by_current_player(self.board[nr][nc]):
                    moves.append(((r, c), (nr, nc)))
        return moves

    def make_move(self, move):
        # Make a move on the board
        (start, end) = move        
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = '.'

    def undo_move(self, move):
        # Undo a move on the board
        (start, end) = move        
        self.board[start[0]][start[1]] = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = '.'


class ChessEngine:
    def __init__(self, board):
        self.board = board

    def evaluate(self):
        # Evaluate the board state (material balance)
        piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
        }
        score = 0
        for row in self.board.board:
            for piece in row:
                if piece in piece_values:
                    score += piece_values[piece]
        return score

    # TODO: Chris: Come up with an enum for is_maximizing.
    def _minimax(self, depth, is_maximizing):
        # Minimax algorithm with fixed depth
        if depth == 0:
            return self.evaluate()

        moves = self.board.generate_moves()
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                self.board.make_move(move)
                eval = self._minimax(depth - 1, is_maximizing=False)
                self.board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                self.board.make_move(move)
                eval = self._minimax(depth - 1, is_maximizing=True)
                self.board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, depth):
        # TODO: ChatGPT: Add stalemate and winner detection.

        # Determine the best move by evaluating all possible moves
        best_move = None
        best_value = float('-inf')
        for move in self.board.generate_moves():
            self.board.make_move(move)
            board_value = self._minimax(depth - 1, False)
            self.board.undo_move(move)
            if board_value > best_value:
                best_value = board_value
                best_move = move
        return best_move

def main():
    # Main function to run the chess engine
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = Board(fen)
    engine = ChessEngine(board)

    while True:
        board.display()
        move = engine.best_move(3)
        if move is None:
            print("Game over")
            break
        board.make_move(move)
        board.turn = Player.BLACK if board.turn == Player.WHITE else Player.WHITE

if __name__ == "__main__":
    main()
