"""
Minimax Algorithm Implementation

This module implements the classic Minimax algorithm for game-playing AI agents.
The Minimax algorithm is a decision-making algorithm used in two-player, zero-sum games
where one player tries to maximize their score while the other tries to minimize it.

Key Features:
- Recursive tree search to evaluate all possible game states
- Alternates between maximizing and minimizing players
- Uses an evaluation function to score terminal or depth-limited states
- Guarantees optimal play assuming both players play perfectly

Author:Wentao Ma
Date Created: July 09, 2025
Version: 1.1

Usage:
    agent = MinimaxAgent(evaluation_function, max_search_depth)
    best_action = agent.get_action(current_game_state)
"""

# minimax_agent.py

class MinimaxAgent:
    def __init__(self, eval_fn, max_depth, mark):
        # Store the evaluation function and maximum search depth for the agent
        self.eval_fn = eval_fn  # Evaluation function
        self.max_depth = max_depth  # Maximum search depth
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'  # Determine opponent's mark
        self.nodes_expanded = 0

    def get_action(self, state):
        # Returns the best action for the current state using the minimax algorithm
        # The agent assumes it is the maximizing player at the root
        self.nodes_expanded = 0
        _, action = self.minimax(state, self.max_depth, True)
        return action

    def minimax(self, state, depth, maximizing_player):
        # Recursive minimax search function
        # state: current game state
        # depth: remaining search depth
        # maximizing_player: True if it's the maximizing player's turn, False otherwise
        self.nodes_expanded += 1

        # Base case: if the state is terminal or depth limit is reached, evaluate the state
        if state.is_terminal() or depth == 0:
            return self.eval_fn(state), None

        if maximizing_player:
            # Maximizing player's turn: try to maximize the evaluation value
            max_eval, best_action = float('-inf'), None
            for action in state.get_legal_actions():
                # Generate the successor state for each legal action
                value, _ = self.minimax(state.generate_successor(action, self.mark), depth - 1, False)
                # Update the best value and action if a better value is found
                if value > max_eval:
                    max_eval, best_action = value, action
            return max_eval, best_action
        else:
            # Minimizing player's turn: try to minimize the evaluation value
            min_eval, best_action = float('inf'), None
            for action in state.get_legal_actions():
                # Generate the successor state for each legal action
                value, _ = self.minimax(state.generate_successor(action, self.opponent_mark), depth - 1, True)
                # Update the best value and action if a lower value is found
                if value < min_eval:
                    min_eval, best_action = value, action
            return min_eval, best_action