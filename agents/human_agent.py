"""
Human Agent:
This agent allows a human player to input their moves in a Tic Tac Toe game through command-line interface (CLI).

Features:
- Prompts the player to enter their move in 'row,col' format
- Validates the move against the current game board
- Re-prompts for input if the move is invalid

No dependencies required.

Date: 2025-07-06
Version: 1.2
"""

class HumanAgent:
    def __init__(self, mark, eval_fn=None, max_depth=None, **kwargs):
        self.mark = mark # 'X' or 'O'
        self.nodes_expanded = 0  # node counter (always zero)

    def get_action(self, board):
        """
        Get the player's move from command-line input
        Args:
            board: The game board
        Returns:
            tuple: (row, col) showing the player's move
        """
        valid_moves = board.get_valid_moves()

        while True:
            try:
                # Get the move as a single string
                move_str = input(f"Player {self.mark}, enter your move as 'row,col' (e.g., '1,2'): ")
                parts = move_str.split(',')
                if len(parts) != 2:
                    raise ValueError("Invalid format. Please use 'row,col'.")

                # Split the input string into row and column
                row = int(parts[0].strip())
                col = int(parts[1].strip())

                # Convert 1-based input to 0-based index for the board (for visualization purposes)
                row_0_indexed = row - 1
                col_0_indexed = col - 1

                # Check if the move is valid
                if board.is_valid_move(row_0_indexed, col_0_indexed):
                    return (row_0_indexed, col_0_indexed)
                else:
                    # print(f"Invalid move! Pick one of moves that are available: {valid_moves}") # debug
                    print(f"Invalid move ({row},{col})! That cell is already taken or out of bounds. Try again.")
            except (ValueError, IndexError):
                print("Invalid format. Please enter your move as 'row,col' (e.g., '1,2').")
