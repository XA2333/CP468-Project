# === Import libraries and modules ===
import time
from typing import Dict, List, Type
from game.board import Board
from game.game import Game
# =========================================

class Metrics:
    def __init__(self) -> None:
        # Store per-game records
        self.records: List[Dict] = []
        # Accumulated wall-clock time
        self._total_time: float = 0.0

    def run_match(self, agent1, agent2, board_size, show_board=False):
        # Create game objects
        board = Board(size=board_size)
        game = Game(board, agent1, agent2)
        move_count = 0

        # Start timer
        start_time = time.time()

        if show_board:
            print(f"\nStarting game: {agent1.mark} vs {agent2.mark}")
            print(f"Initial board:")
            print(game.board)

        while not game.board.is_game_over():
            current_agent = game.get_current_agent()

            if show_board:
                print(f"\nPlayer {game.current_player}'s turn:")

            move = current_agent.get_action(game.board)

            if game.board.make_move(move[0], move[1], game.current_player):
                move_count += 1

                if show_board:
                    print(f"Player {game.current_player} made move: {move}")
                    print(game.board)

                if not game.board.is_game_over():
                    game.switch_player()

        # Stop timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        if show_board:
            winner = game.board.get_winner()
            if winner:
                print(f"\nGame Over! Player {winner} wins!")
            else:
                print("\nIt's a draw!")

        # Update total time
        self._total_time += elapsed_time

        # Build result dict
        result = {
            'winner': game.board.get_winner() or 'Draw',
            'elapsed_sec': elapsed_time,
            'nodes_x': getattr(agent1, 'nodes_expanded', 0),
            'nodes_o': getattr(agent2, 'nodes_expanded', 0),
            'total_moves': move_count
        }

        # Save record
        self.records.append(result)

        # Return result
        return result

    # Run N games and alternate first player
    def run_series(
        self,
        agent_cls_x: Type,
        agent_cls_o: Type,
        games: int = 20,
        board_size: int = 3,
        **agent_kwargs
    ) -> None:

        # Loop over requested game count
        for g in range(games):
            # Even games: X = agent_cls_x, O = agent_cls_o
            if g % 2 == 0:
                ax = agent_cls_x(mark="X", **agent_kwargs)
                ao = agent_cls_o(mark="O", **agent_kwargs)
            # Odd games: swap roles
            else:
                ax = agent_cls_o(mark="X", **agent_kwargs)
                ao = agent_cls_x(mark="O", **agent_kwargs)

            # Run match
            self.run_match(ax, ao, board_size)

    # Return total execution time
    def get_execution_time(self) -> float:
        # Rounded to 4 dp
        return round(self._total_time, 4)

    # Return cumulative node counts
    def get_nodes_evaluated(self) -> Dict[str, int]:
        # Sum nodes for each side
        x_total = sum(r["nodes_x"] for r in self.records)
        o_total = sum(r["nodes_o"] for r in self.records)
        return {"X": x_total, "O": o_total}

    # Return empirical win rates
    def get_success_rate(self) -> Dict[str, float]:
        # Initialise counters
        tally = {"X": 0, "O": 0, "Draw": 0}
        # Count outcomes
        for r in self.records:
            tally[r["winner"]] += 1
        total = len(self.records) or 1
        # Compute proportions
        return {k: round(v / total, 3) for k, v in tally.items()}