# === Import libraries and modules ===
# Place all your import statements here
# =========================================

# === Metrics collector ===
# This module collects and provides various metrics related to the game evaluation.
# It tracks execution time, number of nodes evaluated, and success rate of the agents.
# Feel free to add parameters or adjust these functions as needed
# =========================
import time
from typing import Dict, List, Type
from game.board import Board
from game.game import Game
class Metrics:
    # Constructor
    def __init__(self) -> None:
        # Store per-game records
        self.records: List[Dict] = []
        # Accumulated wall-clock time
        self._total_time: float = 0.0

    # Run a single game and store result
    def run_match(self, agent_x, agent_o, board_size: int = 3) -> Dict:
        # Create game objects
        board = Board(board_size)
        game = Game(board, agent_x, agent_o)
        # Start timer
        t0 = time.perf_counter()
        # Play game
        game.play()
        # Stop timer
        elapsed = time.perf_counter() - t0
        # Update total time
        self._total_time += elapsed
        # Determine winner
        winner = board.get_winner() or "Draw"
        # Build result dict
        result = {
            "winner": winner,
            "elapsed_sec": round(elapsed, 6),
            "nodes_x": getattr(agent_x, "nodes_expanded", 0),
            "nodes_o": getattr(agent_o, "nodes_expanded", 0),
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
