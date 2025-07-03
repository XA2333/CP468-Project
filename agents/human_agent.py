"""
Human Agent: (still need board.py to integrate human input)
This agent allows a human player to input their moves in a Tic Tac Toe game through command-line interface (CLI).

Features:
- Prompts the player to enter their move in 'row,col' format
- Validates the move against the current game board
- Re-prompts for input if the move is invalid

No dependencies required.

Date: 2025-07-03
Version: 1.0
"""
class HumanAgent:
    def __init__(self, mark):
        self.mark = mark # 'X' or 'O'

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

                # Split the input string into row and column
                row, col = map(int, move_str.split(','))

                # Check if the move is valid
                if (row, col) in valid_moves:
                    return (row, col)
                else:
                    print(f"Invalid move! Pick one of moves that are available: {valid_moves}")
            except (ValueError, IndexError):
                print("Invalid format. Please enter your move as 'row,col' (e.g., '1,2').")