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


def square_to_alg(square):
    files = 'abcdefgh'
    ranks = '12345678'
    # TODO: Chris: Figure out the logic of how ranks is converted.
    return files[square[1]] + ranks[(BOARD_SIZE - 1) - square[0]]


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

    def print_legal_moves(self):
        legal_moves = self.generate_moves()
        legal_moves_as_algo = [square_to_alg(start) + square_to_alg(end) for start,end in legal_moves]
        print("Legal moves:\n" + ' '.join(legal_moves_as_algo))

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

    def undo_move(self, move, captured_piece):
        # Undo a move on the board
        (start, end) = move        
        self.board[start[0]][start[1]] = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = captured_piece


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
    # TODO: Instead of changing self.board all the time, we should be passing in a new Board for each
    # call. This way we could easily multithread in the future. And it makes sense that self.board would
    # always refer to the current state, instead of changing around a bunch.
    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.evaluate(), None

        legal_moves = self.board.generate_moves()
        # TODO: Look at pulling the common functionality of the two bodies of this if statement into
        # a common helper function to reduce repeated code.
        if is_maximizing:
            max_eval = -float('inf')
            best_move = None
            for move in legal_moves:
                square_previous_contents = self.board.board[move[1][0]][move[1][1]]
                self.board.make_move(move)
                eval, _ = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board.undo_move(move, square_previous_contents)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                captured_piece = self.board.board[move[1][0]][move[1][1]]
                self.board.make_move(move)
                eval, _ = self.alpha_beta(depth - 1, alpha, beta, True)
                self.board.undo_move(move, captured_piece)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def best_move(self, depth):
        # TODO: ChatGPT: Add stalemate and winner detection.
        _, best_move = self.alpha_beta(depth, -float('inf'), float('inf'), True)
        return best_move

class UCIInterface:
    def __init__(self):
        self.board = None
        self.engine = ChessEngine(self.board)

    def uci(self):
        print("id name SimpleChessEngine")
        print("id author SCRB")
        print("uciok")

    def isready(self):
        print("readyok")

    def position(self, fen):
        self.board = Board(fen)
        self.engine = ChessEngine(self.board)

    def go(self, depth):
        best_move = self.engine.best_move(depth)
        start, end = best_move
        move_str = square_to_alg(start) + square_to_alg(end)
        print(f"bestmove {move_str}")

    def print_board(self):
        self.board.display()
        self.board.print_legal_moves()

    def run(self):
        while True:
            try:
                # TODO: Have this loop just handle routing the commands to the
                # right functions, and those function then parse the command string
                # as needed.
                command = input().strip()
                if command == "uci":
                    self.uci()
                elif command == "isready":
                    self.isready()
                elif command.startswith("position startpos"):
                    # TODO: ChatGPT: handles moves passed in with this command.
                    start_pos_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                    self.position(start_pos_fen)
                elif command.startswith("position fen"):
                    # TODO: ChatGPT: handles moves passed in with this command.
                    fen = command.split("position fen ")[1]
                    self.position(fen)
                elif command.startswith("go depth"):
                    depth = int(command.split("go depth ")[1])
                    self.go(depth)
                elif command == "d":
                    self.print_board()
                elif command == "quit":
                    break
            except EOFError:
                break


if __name__ == "__main__":
    uci_interface = UCIInterface()
    uci_interface.run()

