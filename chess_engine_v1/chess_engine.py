class Board:
    def __init__(self, fen):
        # Initialize the board using FEN notation
        self.board = self.parse_fen(fen)
        self.turn = 'w'  # 'w' for white, 'b' for black

    def parse_fen(self, fen):
        # Parse the FEN string to set up the board
        board = []
        rows = fen.split(' ')[0].split('/')
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(['.'] * int(char))
                else:
                    board_row.append(char)
            board.append(board_row)
        return board

    def display(self):
        # Print the board state
        for row in self.board:
            print(' '.join(row))
        print()

    # Added by Chris.
    def square_to_alg(self, square):
        files = 'abcdefgh'
        ranks = '12345678'
        return files[square[1]] + ranks[7 - square[0]]

    def print_legal_moves(self):
        legal_moves = self.generate_moves()
        legal_moves_as_algo = [self.square_to_alg(start) + self.square_to_alg(end) for start,end in legal_moves]
        print("Legal moves:\n" + ' '.join(legal_moves_as_algo))

    def generate_moves(self):
        # Generate all legal moves for the current player
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece.isupper() if self.turn == 'w' else piece.islower():
                    moves.extend(self.generate_piece_moves(piece, r, c))
        return moves

    def generate_piece_moves(self, piece, r, c):
        # Generate legal moves for a specific piece
        if piece.upper() == 'P':
            return self.generate_pawn_moves(piece, r, c)
        elif piece.upper() == 'R':
            return self.generate_rook_moves(piece, r, c)
        elif piece.upper() == 'N':
            return self.generate_knight_moves(piece, r, c)
        elif piece.upper() == 'B':
            return self.generate_bishop_moves(piece, r, c)
        elif piece.upper() == 'Q':
            return self.generate_queen_moves(piece, r, c)
        elif piece.upper() == 'K':
            return self.generate_king_moves(piece, r, c)
        return []

    def generate_pawn_moves(self, piece, r, c):
        # Generate legal pawn moves
        moves = []
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1

        # Single square move
        if self.board[r + direction][c] == '.':
            moves.append(((r, c), (r + direction, c)))
            # Double square move
            if r == start_row and self.board[r + 2 * direction][c] == '.':
                moves.append(((r, c), (r + 2 * direction, c)))

        # Captures
        for dc in [-1, 1]:
            if 0 <= c + dc < 8 and self.board[r + direction][c + dc] != '.' and self.board[r + direction][c + dc].islower() != piece.islower():
                moves.append(((r, c), (r + direction, c + dc)))
        
        return moves

    def generate_rook_moves(self, piece, r, c):
        # Generate legal rook moves
        return self.generate_sliding_moves(piece, r, c, [(0, 1), (1, 0), (0, -1), (-1, 0)])

    def generate_bishop_moves(self, piece, r, c):
        # Generate legal bishop moves
        return self.generate_sliding_moves(piece, r, c, [(1, 1), (1, -1), (-1, -1), (-1, 1)])

    def generate_queen_moves(self, piece, r, c):
        # Generate legal queen moves
        return self.generate_sliding_moves(piece, r, c, [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])

    def generate_sliding_moves(self, piece, r, c, directions):
        # Generate sliding moves for rooks, bishops, and queens
        moves = []
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == '.':
                        moves.append(((r, c), (nr, nc)))
                    elif self.board[nr][nc].islower() != piece.islower():
                        moves.append(((r, c), (nr, nc)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def generate_knight_moves(self, piece, r, c):
        # Generate legal knight moves
        moves = []
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == '.' or self.board[nr][nc].islower() != piece.islower():
                    moves.append(((r, c), (nr, nc)))
        return moves

    def generate_king_moves(self, piece, r, c):
        # Generate legal king moves
        moves = []
        king_moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in king_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == '.' or self.board[nr][nc].islower() != piece.islower():
                    moves.append(((r, c), (nr, nc)))
        return moves

    def make_move(self, move):
        # Make a move on the board
        (start, end) = move
        piece = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = '.'
        self.board[end[0]][end[1]] = piece

    def undo_move(self, move, captured_piece):
        # Undo a move on the board
        (start, end) = move
        piece = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = captured_piece
        self.board[start[0]][start[1]] = piece

    def evaluate(self):
        # Evaluate the board state (material balance)
        piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
        }
        score = 0
        for row in self.board:
            for piece in row:
                if piece in piece_values:
                    score += piece_values[piece]
        return score

class ChessEngine:
    def __init__(self, board):
        self.board = board

    def alpha_beta(self, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.board.evaluate(), None

        legal_moves = self.board.generate_moves()
        if is_maximizing:
            max_eval = -float('inf')
            best_move = None
            for move in legal_moves:
                captured_piece = self.board.board[move[1][0]][move[1][1]]
                self.board.make_move(move)
                eval, _ = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board.undo_move(move, captured_piece)
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
        _, best_move = self.alpha_beta(depth, -float('inf'), float('inf'), True)
        return best_move

class UCIInterface:
    def __init__(self):
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.engine = ChessEngine(self.board)

    def uci(self):
        print("id name SimpleChessEngine")
        print("id author YourName")
        print("uciok")

    def isready(self):
        print("readyok")

    def position(self, fen):
        self.board = Board(fen)
        self.engine = ChessEngine(self.board)

    def go(self, depth):
        best_move = self.engine.best_move(depth)
        start, end = best_move
        move_str = self.square_to_alg(start) + self.square_to_alg(end)
        print(f"bestmove {move_str}")

    def square_to_alg(self, square):
        files = 'abcdefgh'
        ranks = '12345678'
        return files[square[1]] + ranks[7 - square[0]]

    def print_board(self):
        self.board.display()
        self.board.print_legal_moves()

    def run(self):
        while True:
            try:
                command = input().strip()
                if command == "uci":
                    self.uci()
                elif command == "isready":
                    self.isready()
                elif command.startswith("position fen"):
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
