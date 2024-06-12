import subprocess
import time

class SelfPlay:
    def __init__(self, engine_command):
        self.engine_command = engine_command

    def start_engine(self):
        """
        Start a chess engine subprocess.
        """
        return subprocess.Popen(
            self.engine_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # Chris change for better debugging.
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

    def send_command(self, engine, command):
        """
        Send a command to a chess engine.
        """
        print(f"Sending command: {command}")
        engine.stdin.write(command + '\n')
        engine.stdin.flush()

    def read_response(self, engine):
        """
        Read the response from a chess engine.
        """
        response = ""
        while True:
            line = engine.stdout.readline().strip()
            if line:
                print(f"Received response: {line}")
                response += line + "\n"
                if line.startswith("bestmove") or line == "uciok" or line == "readyok":
                    break
        return response

    def read_board(self, engine):
        """
        Read the board state from the engine and print it.
        """
        self.send_command(engine, "d")

        while True:
            line = engine.stdout.readline().strip()
            if line == "Legal moves:":
                break
            # Chris: Flush to help debug.
            print(line, flush=True)



    def play_game(self, max_moves=100):
        """
        Play a game between two engines, alternating moves until a move limit is reached or no valid moves are found.
        """
        # Start both engines
        engine1 = self.start_engine()
        engine2 = self.start_engine()

        # Initialize engines with UCI protocol
        for engine in [engine1, engine2]:
            self.send_command(engine, "uci")
            self.read_response(engine)
            self.send_command(engine, "isready")
            self.read_response(engine)

        # Set the starting position
        starting_fen = "position startpos"
        self.send_command(engine1, starting_fen)
        self.send_command(engine2, starting_fen)

        # Play the game
        current_engine = engine1
        next_engine = engine2
        move_history = []

        for move_count in range(max_moves):
            self.send_command(current_engine, "go depth 2")
            response = self.read_response(current_engine)
            if "bestmove" in response:
                best_move = response.split("bestmove ")[1].split(" ")[0]
                move_history.append(best_move)
                print(f"Move {move_count + 1}: {best_move}")

                # Send the move to the next engine
                position_command = f"position startpos moves {' '.join(move_history)}"
                self.send_command(next_engine, position_command)

                # Print the current board state
                self.read_board(current_engine)

                # Switch engines
                current_engine, next_engine = next_engine, current_engine
            else:
                print("No valid move found. Game over.")
                break

        # Terminate both engines
        engine1.terminate()
        engine2.terminate()

if __name__ == "__main__":
    engine_command = ["..\\run_python.bat", "chess_engine.py"]
    game = SelfPlay(engine_command)
    game.play_game()
