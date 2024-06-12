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

    def undo_move(self, move):
        # Undo a move on the board
        (start, end) = move
        piece = self.board[end[0]][end[1]]
        self.board[end[0]][end[1]] = '.'
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

    def minimax(self, depth, is_maximizing):
        # Minimax algorithm with fixed depth
        if depth == 0:
            return self.board.evaluate()

        moves = self.board.generate_moves()
        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                self.board.make_move(move)
                eval = self.minimax(depth - 1, False)
                self.board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                self.board.make_move(move)
                eval = self.minimax(depth - 1, True)
                self.board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self, depth):
        # Determine the best move by evaluating all possible moves
        best_move = None
        best_value = float('-inf')
        for move in self.board.generate_moves():
            self.board.make_move(move)
            board_value = self.minimax(depth - 1, False)
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
        board.turn = 'b' if board.turn == 'w' else 'w'

if __name__ == "__main__":
    main()
