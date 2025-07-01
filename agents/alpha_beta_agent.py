"""
Alpha-Beta Pruning Algorithm Implementation

This module implements the Alpha-Beta pruning algorithm, an optimization of the 
Minimax algorithm for game-playing AI agents. Alpha-Beta pruning reduces the 
number of nodes evaluated in the search tree by eliminating branches that 
cannot possibly influence the final decision.

Key Features:
- Optimized version of Minimax with significant performance improvements
- Uses alpha and beta bounds to prune unnecessary branches
- Maintains the same optimal decision-making as Minimax
- Dramatically reduces computational complexity in most cases
- Particularly effective with good move ordering

Algorithm Details:
- Alpha: Best value that the maximizing player can guarantee
- Beta: Best value that the minimizing player can guarantee
- Pruning occurs when alpha >= beta (no need to explore further)

Author: Game AI Course - CP468
Date Created: 2025
Version: 1.0

Usage:
    agent = AlphaBetaAgent(evaluation_function, max_search_depth)
    best_action = agent.get_action(current_game_state)
"""

# alpha_beta_agent.py

import math

class AlphaBetaAgent:
    def __init__(self, eval_fn, max_depth):
        self.eval_fn = eval_fn  # Evaluation function used to score states
        self.max_depth = max_depth  # Maximum depth to search in the game tree

    def get_action(self, state):
        # Returns the best action for the current state using alpha-beta pruning
        # Calls the alpha_beta recursive function starting from the root
        _, action = self.alpha_beta(state, self.max_depth, float('-inf'), float('inf'), True)
        return action

    def alpha_beta(self, state, depth, alpha, beta, maximizing_player):
        # Base case: if the state is terminal or depth limit reached, evaluate the state
        if state.is_terminal() or depth == 0:
            return self.eval_fn(state), None

        if maximizing_player:
            # Maximizing player's turn
            value, best_action = float('-inf'), None
            # Iterate over all possible legal actions
            for action in state.get_legal_actions():
                successor = state.generate_successor(action)
                new_value, _ = self.alpha_beta(successor, depth - 1, alpha, beta, False)
                if new_value > value:
                    value, best_action = new_value, action
                # Update alpha with the best value found so far
                alpha = max(alpha, value)
                # Beta cut-off: prune the remaining branches
                if alpha >= beta:
                    break
            return value, best_action
        else:
            # Minimizing player's turn
            value, best_action = float('inf'), None
            for action in state.get_legal_actions():
                successor = state.generate_successor(action)
                new_value, _ = self.alpha_beta(successor, depth - 1, alpha, beta, True)
                if new_value < value:
                    value, best_action = new_value, action
                # Update beta with the lowest value found so far
                beta = min(beta, value)
                # Alpha cut-off: prune the remaining branches
                if beta <= alpha:
                    break
            return value, best_action
