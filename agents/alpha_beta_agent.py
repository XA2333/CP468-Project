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

Author:Wentao Ma
Date Created: July 16, 2025
Version: 1.2

Usage:
    agent = AlphaBetaAgent(evaluation_function, max_search_depth)
    best_action = agent.get_action(current_game_state)
"""

# alpha_beta_agent.py

import math
from visualization.tree_diagram import Node


class AlphaBetaAgent:
    def __init__(self, eval_fn, max_depth, mark):
        self.eval_fn = eval_fn  # Evaluation function used to score states
        self.max_depth = max_depth  # Max search depth
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
        self.nodes_expanded = 0
        self.last_search_tree = None  # Store root Node for visualization

    def get_action(self, state):
        # Returns the best action for the current state using alpha-beta pruning
        # Calls the alpha_beta recursive function starting from the root
        self.nodes_expanded = 0

        # Create root node of the search tree
        root_node = Node(
            move=None,
            value=None,
            alpha=float('-inf'),
            beta=float('inf'),
            is_max=True,
            pruned=False
        )

        # Run alpha-beta with tree building
        value, action = self.alpha_beta(state, self.max_depth, float(
            '-inf'), float('inf'), True, root_node)

        # Store root node for visualization after move
        self.last_search_tree = root_node

        return action

    def alpha_beta(self, state, depth, alpha, beta, maximizing_player, parent_node):
        # Base case: if the state is terminal or depth limit reached, evaluate the state
        self.nodes_expanded += 1

        # Terminal or depth limit: evaluate node and set value
        if state.is_terminal() or depth == 0:
            val = self.eval_fn(state)
            parent_node.value = val
            return val, None

        if maximizing_player:
            # Maximizing player's turn
            value, best_action = float('-inf'), None
            # Iterate over all possible legal actions
            for action in state.get_legal_actions():
                successor = state.generate_successor(action, self.mark)

                # Create child node
                child_node = Node(
                    move=action,
                    value=None,
                    alpha=alpha,
                    beta=beta,
                    is_max=False,
                    pruned=False
                )
                parent_node.add_child(child_node)

                new_value, _ = self.alpha_beta(
                    successor, depth - 1, alpha, beta, False, child_node)

                if new_value > value:
                    value, best_action = new_value, action

                # Update alpha
                alpha = max(alpha, value)
                child_node.value = new_value
                child_node.alpha = alpha
                child_node.beta = beta

                # Prune if possible
                if alpha >= beta:
                    # Mark remaining siblings as pruned
                    # Note: pruning means stopping exploration here; mark remaining children pruned
                    siblings = state.get_legal_actions()
                    prune_index = siblings.index(action)
                    for rem_action in siblings[prune_index+1:]:
                        pruned_node = Node(
                            move=rem_action,
                            value=None,
                            alpha=alpha,
                            beta=beta,
                            is_max=False,
                            pruned=True
                        )
                        parent_node.add_child(pruned_node)
                    break

            parent_node.value = value
            return value, best_action

        else:
            # Minimizing player's turn
            value, best_action = float('inf'), None

            for action in state.get_legal_actions():
                successor = state.generate_successor(
                    action, self.opponent_mark)

                child_node = Node(
                    move=action,
                    value=None,
                    alpha=alpha,
                    beta=beta,
                    is_max=True,
                    pruned=False
                )
                parent_node.add_child(child_node)

                new_value, _ = self.alpha_beta(
                    successor, depth - 1, alpha, beta, True, child_node)

                if new_value < value:
                    value, best_action = new_value, action

                beta = min(beta, value)
                child_node.value = new_value
                child_node.alpha = alpha
                child_node.beta = beta

                if beta <= alpha:
                    siblings = state.get_legal_actions()
                    prune_index = siblings.index(action)
                    for rem_action in siblings[prune_index+1:]:
                        pruned_node = Node(
                            move=rem_action,
                            value=None,
                            alpha=alpha,
                            beta=beta,
                            is_max=True,
                            pruned=True
                        )
                        parent_node.add_child(pruned_node)
                    break

            parent_node.value = value
            return value, best_action
