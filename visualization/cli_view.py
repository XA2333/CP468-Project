# === Import libraries and modules ===
# Place all your import statements here
# =========================================
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.board import Board
from game.game import Game
from agents.human_agent import HumanAgent
from agents.minimax_agent import MinimaxAgent
from agents.alpha_beta_agent import AlphaBetaAgent
from agents.expectiminimax_agent import ExpectiminimaxAgent
try:
    from agents.gemini_agent import GeminiAgent
except ImportError:
    GeminiAgent = None

def eval_fn(board):
    winner = board.get_winner()
    return 1 if winner == 'O' else (-1 if winner == 'X' else 0)

def select_agent(mark):
    options = [
        ("Human",      lambda: HumanAgent(mark=mark)),
        ("Minimax",    lambda: MinimaxAgent(mark=mark, eval_fn=eval_fn, max_depth=9)),
        ("Alpha-Beta", lambda: AlphaBetaAgent(eval_fn=eval_fn, max_depth=9, mark=mark)),
        ("ExpectiMin", lambda: ExpectiminimaxAgent(eval_fn=eval_fn, max_depth=9, mark=mark)),
    ]
    if GeminiAgent:
        options.append(("Gemini", lambda: GeminiAgent(mark=mark, eval_fn=eval_fn, max_depth=9)))

    print(f"Select opponent for Player {mark}:")
    for i, (name, _) in enumerate(options, start=1):
        print(f"  {i}. {name}")

    while True:
        choice = input(f"Enter choice [1-{len(options)}]: ")
        if choice.isdigit() and 1 <= (c := int(choice)) <= len(options):
            return options[c-1][1]()
        print("Invalid choice, try again.")

class CLIView:
    def __init__(self, board_size=3, agent1=None, agent2=None):
        self.board = Board(size=board_size)
        self.agent1 = agent1 or HumanAgent(mark='X')
        self.agent2 = agent2 or HumanAgent(mark='O')
        self.game = Game(self.board, self.agent1, self.agent2)

    def display_board(self):
        state = self.board.get_state()
        size = self.board.size
        header = '   ' + ' '.join(str(i+1) for i in range(size))
        print(header)
        for r in range(size):
            row_vals = [(state[r][c] or '.') for c in range(size)]
            print(f"{r+1}  " + ' '.join(row_vals))
        print()

    def run(self):
        print("Welcome to Tic-Tac-Toe (CLI)!")
        while not self.board.is_game_over():
            self.display_board()
            current = self.game.current_player
            print(f"Player {current}'s turn.")
            agent = self.game.get_current_agent()
            move = agent.get_action(self.board)
            row, col = move
            if not self.board.make_move(row, col, current):
                print(f"Invalid move at ({row+1},{col+1}). Try again.")
                continue
            self.game.switch_player()

        self.display_board()
        winner = self.board.get_winner()
        if winner:
            print(f"Game Over: Player {winner} wins!")
        else:
            print("Game Over: It's a draw.")

if __name__ == '__main__':
    opp = select_agent(mark='O')      # <-- now Pylance sees this function!
    view = CLIView(agent1=HumanAgent('X'), agent2=opp)
    view.run()
