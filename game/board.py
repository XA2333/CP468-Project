# === Import libraries and modules ===
import numpy as np
# =========================================

# === Board class definition ===
# This class represents the game board and contains methods to manage the game state.
# It includes methods to check for valid moves, make moves, check for a win, and reset the board.
# Feel free to add parameters or adjust these functions as needed
# =========================
class Board:
  def __init__(self, size=3):
    self.size = size
    self.board = np.full((size, size), None)
    self.winning_length = 3 if size == 3 else 5
    self.move_log = []
    self.total_move = 0

  def is_valid_move(self, row, col):
    # Checks if a move (row, col) is within bounds and the cell is empty
    return 0 <= row < self.size and \
            0 <= col < self.size and \
            self.board[row, col] is None

  def get_valid_moves(self):
    # Returns a list of all valid (empty) moves on the board
    valid_moves = []
    for row in range(self.size):
        for col in range(self.size):
            if self.board[row, col] is None:
                valid_moves.append((row, col))
    return valid_moves

  def is_full(self):
    # Checks if the board is full (no empty cells)
    return len(self.get_valid_moves()) == 0

  def is_terminal(self):
    # Checks if the current board state is terminal (game over)
    return self.is_game_over()

  def get_legal_actions(self):
    # Returns a list of legal actions (valid moves) from the current state
    return self.get_valid_moves()

  def generate_successor(self, action, current_player_mark):
    # Generates a new Board state by applying the action for the current_player_mark
    row, col = action

    new_board = Board(self.size)
    new_board.board = self.board.copy()
    new_board.winning_length = self.winning_length

    # Apply the move to the new board
    new_board.board[row, col] = current_player_mark
    return new_board

  def check_win(self, mark):
    # Check rows (horizontal wins)
    for row in range(self.size):
        for col in range(self.size - self.winning_length + 1):
            if all(self.board[row, col+i] == mark for i in range(self.winning_length)):
                return True

    # Check columns (vertical wins)
    for col in range(self.size):
        for row in range(self.size - self.winning_length + 1):
            if all(self.board[row+i, col] == mark for i in range(self.winning_length)):
                return True

    # Check diagonals (down-right wins)
    for row in range(self.size - self.winning_length + 1):
        for col in range(self.size - self.winning_length + 1):
            if all(self.board[row+i, col+i] == mark for i in range(self.winning_length)):
                return True

    # Check diagonals (up-right wins)
    for row in range(self.winning_length - 1, self.size):
        for col in range(self.size - self.winning_length + 1):
            if all(self.board[row-i, col+i] == mark for i in range(self.winning_length)):
                return True

    return False

  def make_move(self, row, col, mark):
    # Attempts to make a move at (row, col) with the given mark ('X' or 'O').
    if not self.is_valid_move(row, col):
        return False

    self.board[row, col] = mark
    self.move_log.append((row, col, mark))
    self.total_move += 1
    return True

  def is_game_over(self):
    # Checks if the game is over (either a win or a draw)
    return self.get_winner() is not None or self.is_full()

  def get_winner(self):
    # Returns the mark of the winning player if there is one, otherwise None.
    if self.check_win('X'):
        return 'X'
    elif self.check_win('O'):
        return 'O'
    else:
        return None

  def get_state(self, row=None, col=None):
    # Returns the current state of the board.
    return self.board.copy()

  # def get_current_player(): pass - implemented in Game class
  # def reset(): pass

  def __str__(self):
    str = ""
    for row in range(self.size):
        str += "|"
        for col in range(self.size):
            cell_value = self.board[row, col]
            # Display 'X', 'O' or '.' for empty cells
            str += f" {cell_value if cell_value is not None else '.'} |"
        str += "\n"
    return str