import fen
from board import Board
from move import Move


class ChessEngine:
    def __init__(self, board: Board):
        self.board = board

    def evaluate(self) -> int:
        # Evaluate the board state (material balance)
        piece_values = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 1000,
            "p": -1,
            "n": -3,
            "b": -3,
            "r": -5,
            "q": -9,
            "k": -1000,
        }
        score = 0
        for row in self.board.board:
            for piece in row:
                if piece in piece_values:
                    score += piece_values[piece]
        return score

    # TODO: Chris: Come up with an enum for is_maximizing.
    # TODO: Instead of changing self.board all the time, we should be passing in a new
    # Board for each call. This way we could easily multithread in the future. And it
    # makes sense that self.board would always refer to the current state, instead of
    # changing around a bunch.
    def alpha_beta(
        self, depth: int, alpha: float, beta: float, is_maximizing: bool
    ) -> tuple[float, Move | None]:
        if depth == 0:
            return self.evaluate(), None

        legal_moves = self.board.generate_moves()
        # TODO: Look at pulling the common functionality of the two bodies of this if
        # statement into a common helper function to reduce repeated code.
        if is_maximizing:
            max_eval = -float("inf")
            best_move = None
            for move in legal_moves:
                self.board.make_move(move)
                eval, _ = self.alpha_beta(depth - 1, alpha, beta, False)  # noqa
                self.board.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in legal_moves:
                self.board.make_move(move)
                eval, _ = self.alpha_beta(depth - 1, alpha, beta, True)  # noqa
                self.board.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def best_move(self, depth: int) -> Move | None:
        # TODO: ChatGPT: Add stalemate and winner detection.
        _, best_move = self.alpha_beta(depth, -float("inf"), float("inf"), True)
        return best_move


def uci_algebraic_notation(move: Move) -> str:
    val = f"{move.start}{move.end}"
    if move.promotion_piece:
        val += move.promotion_piece.lower()
    return val


class UCIInterface:
    def __init__(self) -> None:
        self.board = None
        self.engine = ChessEngine(self.board)  # type: ignore

    def uci(self) -> None:
        print("id name SimpleChessEngine")
        print("id author SCRB")
        print("uciok")

    def isready(self) -> None:
        print("readyok")

    def position(self, fen: str) -> None:
        self.board = Board(fen)  # type: ignore
        self.engine = ChessEngine(self.board)  # type: ignore

    def go(self, depth: int) -> None:
        best_move = self.engine.best_move(depth)
        move_in_uci_alge = uci_algebraic_notation(best_move)  # type: ignore
        print(f"bestmove {move_in_uci_alge}")

    def print_board(self) -> None:
        self.board.display()  # type: ignore
        self.board.print_legal_moves()  # type: ignore

    def run(self) -> None:
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
                    self.position(fen.STARTING_GAME_FEN)
                elif command.startswith("position fen"):
                    # TODO: ChatGPT: handles moves passed in with this command.
                    fen_str = command.split("position fen ")[1]
                    self.position(fen_str)
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
