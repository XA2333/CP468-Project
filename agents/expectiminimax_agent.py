"""
Expectiminimax Algorithm Implementation

This module implements the Expectiminimax algorithm for game-playing AI agents
in environments with uncertainty. Unlike the standard Minimax algorithm,
Expectiminimax handles games with chance nodes (random events) by computing
expected values instead of assuming worst-case scenarios.

Key Features:
- Handles three types of nodes: Max, Min, and Chance
- Computes expected values for probabilistic outcomes
- Suitable for games with random elements (dice, card draws, etc.)
- Provides optimal play against uncertain opponents
- Uses probability distributions to model random events

Algorithm Structure:
- Max nodes: Choose action that maximizes expected value
- Min nodes: Choose action that minimizes expected value
- Chance nodes: Compute weighted average of all possible outcomes

Applications:
- Board games with dice (Backgammon, Monopoly)
- Card games with hidden information
- Games with random events or uncertain opponent behavior

Author: Game AI Course - CP468
Date Created: 2025
Version: 1.0

Usage:
    agent = ExpectiminimaxAgent(evaluation_function, max_search_depth)
    best_action = agent.get_action(current_game_state)
"""

# expectiminimax_agent.py

import random

class ExpectiminimaxAgent:
    def __init__(self, eval_fn, max_depth, mark):
        self.eval_fn = eval_fn  # Evaluation function used to evaluate terminal/non-terminal states
        self.max_depth = max_depth  # Maximum search depth for the algorithm
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
        self.nodes_expanded = 0  # node counter

    def get_action(self, state):
        # Returns the best action for the current state using the expectiminimax algorithm
        # Only the action part is returned; the value is ignored here
        _, action = self.expectiminimax(state, self.max_depth, "max")
        return action

    def expectiminimax(self, state, depth, node_type):
        # Recursive expectiminimax search
        # state: current game state
        # depth: remaining search depth
        # node_type: "max", "min", or "chance" indicating the type of node

        # Base case: if the state is terminal or depth limit reached, evaluate the state
        self.nodes_expanded += 1  # increment counter
        if state.is_terminal() or depth == 0:
            return self.eval_fn(state), None

        if node_type == "max":
            # Maximizing player's turn: choose the action with the highest expected value
            max_eval, best_action = float('-inf'), None
            for action in state.get_legal_actions():
                # For each action, simulate the result and evaluate using expectiminimax
                value, _ = self.expectiminimax(state.generate_successor(action, self.opponent_mark), depth - 1, "chance")
                if value > max_eval:
                    max_eval, best_action = value, action
            return max_eval, best_action

        elif node_type == "min":
            # Minimizing player's turn: choose the action with the lowest expected value
            min_eval, best_action = float('inf'), None
            for action in state.get_legal_actions():
                # For each action, simulate the result and evaluate using expectiminimax
                value, _ = self.expectiminimax(state.generate_successor(action, self.mark), depth - 1, "chance")
                if value < min_eval:
                    min_eval, best_action = value, action
            return min_eval, best_action

        elif node_type == "chance":
            # Chance node: calculate the expected value over all possible actions
            total_value = 0
            actions = state.get_legal_actions()
            prob = 1 / len(actions)  # Assume uniform probability distribution over actions
            for action in actions:
                # For each possible outcome, calculate its expected value
                value, _ = self.expectiminimax(state.generate_successor(action, self.mark), depth - 1, "min")
                total_value += prob * value
            return total_value, None
