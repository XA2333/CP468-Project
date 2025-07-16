# visualization/tree_diagram.py

import matplotlib.pyplot as plt
import networkx as nx
import os
from datetime import datetime


class Node:
    def __init__(self, move=None, value=None, alpha=None, beta=None, is_max=None, pruned=False):
        self.move = move  # (row, col)
        self.value = value  # Utility value
        self.alpha = alpha
        self.beta = beta
        self.is_max = is_max  # Maximizing or minimizing
        self.pruned = pruned
        self.children = []
        self.parent = None
        self.id = id(self)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


class TreeDiagram:
    def __init__(self, root):
        self.root = root

    def draw(self, title="Alpha-Beta Pruning Tree"):
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()
        labels = {}
        pos = {}
        node_levels = {}

        # Define format_val early so it's available in the loop
        def format_val(val):
            if val == float('inf'):
                return '∞'
            elif val == float('-inf'):
                return '-∞'
            elif val is None:
                return '-'
            else:
                return f"{val: .1f}"

        # Assign level (depth) and gather nodes level by level
        def assign_levels(node, depth=0):
            node_levels.setdefault(depth, []).append(node)
            for child in node.children:
                assign_levels(child, depth + 1)

        assign_levels(self.root)

        # Assign x positions to each node in each level (balanced spacing)
        for depth, nodes in node_levels.items():
            count = len(nodes)
            for i, node in enumerate(nodes):
                x = i - count / 2  # space nodes evenly around x=0
                y = -depth
                pos[node.id] = (x, y)

                alpha_str = format_val(node.alpha)
                beta_str = format_val(node.beta)
                labels[node.id] = f"{'MAX' if node.is_max else 'MIN'}\n{node.move}\nV: {node.value}\nα: {alpha_str} β: {beta_str}"

                for child in node.children:
                    G.add_edge(node.id, child.id,
                               color='red' if child.pruned else 'black')

        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        node_colors = []
        for n in G.nodes():
            node_obj = None
            # Find node object by ID
            for level_nodes in node_levels.values():
                for node in level_nodes:
                    if node.id == n:
                        node_obj = node
                        break
                if node_obj:
                    break
            # Assign color based on pruning status
            if node_obj is not None:
                if node_obj.pruned:
                    node_colors.append('red')
                elif node_obj == self.root:
                    node_colors.append('lightgreen')
                else:
                    node_colors.append('skyblue')
            else:
                node_colors.append('gray')  # fallback


        plt.figure(figsize=(14, 8))
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=2500,
                node_color=node_colors, edge_color=edge_colors,
                font_size=7, font_weight='bold', arrows=True)

        plt.title(title)
        plt.axis('off')
        plt.tight_layout()

        # Create the "pruning visualization" folder if it doesn't exist
        save_folder = "pruning visualization"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
        filename = f"alpha_beta_tree_{timestamp}.png"
        filepath = os.path.join(save_folder, filename)

        # Save the figure
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {filepath}")

        plt.show()
