# === Import libraries and modules ===
# Place all your import statements here
# =========================================
from game.game import Game
from game.board import Board
import pygame
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from agents.gemini_agent import GeminiAgent
except ImportError:
    GeminiAgent = None

# Config
CELL_SIZE = 100
LINE_WIDTH = 4
WINDOW_BG = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# Simple evaluation function


def eval_fn(board):
    winner = board.get_winner()
    if winner == 'O': return 1
    if winner == 'X': return -1
    return 0

# Same select_agent helper for GUI


def select_agent(mark):
    # ===== Import agents locally to avoid circular imports =====
    from agents.expectiminimax_agent import ExpectiminimaxAgent
    from agents.alpha_beta_agent import AlphaBetaAgent
    from agents.minimax_agent import MinimaxAgent
    from agents.human_agent import HumanAgent

    options = [
        ("Human", lambda: HumanAgent(mark=mark)),
        ("Minimax", lambda: MinimaxAgent(mark=mark, eval_fn=eval_fn, max_depth=9)),
        ("Alpha-Beta", lambda: AlphaBetaAgent(eval_fn=eval_fn, max_depth=9, mark=mark)),
        ("Expectiminimax", lambda: ExpectiminimaxAgent(eval_fn=eval_fn, max_depth=9, mark=mark)),
    ]
    if GeminiAgent:
        options.append(("Gemini", lambda: GeminiAgent(mark=mark, eval_fn=eval_fn, max_depth=9)))

    print(f"Select opponent for Player X:")
    for idx, (name, _) in enumerate(options, start=1):
        print(f"  {idx}. {name}")
    while True:
        choice = input(f"Enter choice [1-{len(options)}]: ")
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx-1][1]()
        print("Invalid choice, try again.")


class GUIView:
    def __init__(self, board_size=3, agent1=None, agent2=None):
        # ===== Import agents locally to avoid circular imports =====
        from agents.human_agent import HumanAgent

        pygame.init()
        self.board = Board(size=board_size)
        self.agent1 = agent1 or HumanAgent(mark='X')
        self.agent2 = agent2 or HumanAgent(mark='O')
        self.game = Game(self.board, self.agent1, self.agent2)
        self.size = board_size
        self.window_size = CELL_SIZE * self.size
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.running = True

    def draw_grid(self):
        for i in range(1, self.size):
            pygame.draw.line(self.screen, LINE_COLOR,
                             (i * CELL_SIZE, 0), (i * CELL_SIZE, self.window_size), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR,
                             (0, i * CELL_SIZE), (self.window_size, i * CELL_SIZE), LINE_WIDTH)

    def draw_marks(self):
        state = self.board.get_state()
        for r in range(self.size):
            for c in range(self.size):
                mark = state[r][c]
                if mark:
                    center = (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                    if mark == 'X':
                        offset = CELL_SIZE // 4
                        pygame.draw.line(self.screen, X_COLOR,
                                         (center[0] - offset, center[1] - offset),
                                         (center[0] + offset, center[1] + offset), LINE_WIDTH)
                        pygame.draw.line(self.screen, X_COLOR,
                                         (center[0] - offset, center[1] + offset),
                                         (center[0] + offset, center[1] - offset), LINE_WIDTH)
                    else:
                        pygame.draw.circle(self.screen, O_COLOR,
                                           center, CELL_SIZE // 3, LINE_WIDTH)

    def run(self):
        # ===== Import agents locally to avoid circular imports =====
        from agents.human_agent import HumanAgent

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.is_game_over():
                    agent = self.game.get_current_agent()
                    if isinstance(agent, HumanAgent):
                        x, y = pygame.mouse.get_pos()
                        row, col = y // CELL_SIZE, x // CELL_SIZE
                        if self.board.make_move(row, col, self.game.current_player):
                            self.game.switch_player()

            # AI turn
            if not self.board.is_game_over():
                agent = self.game.get_current_agent()
                if not isinstance(agent, HumanAgent):
                    row, col = agent.get_action(self.board)
                    if self.board.make_move(row, col, self.game.current_player):
                        self.game.switch_player()

            self.screen.fill(WINDOW_BG)
            self.draw_grid()
            self.draw_marks()
            pygame.display.flip()

            if self.board.is_game_over():
                winner = self.board.get_winner()
                print(f"Game Over: {'Draw' if not winner else f'Player {winner} wins!'}")
                self.running = False

        pygame.quit()


if __name__ == '__main__':
    # ===== Import agents locally to avoid circular imports =====
    from agents.human_agent import HumanAgent

    opp = select_agent(mark='O')
    view = GUIView(agent1=HumanAgent(mark='X'), agent2=opp)
    view.run()
