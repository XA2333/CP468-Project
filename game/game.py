# === Import libraries and modules ===
# Place all your import statements here
# =========================================

# === Game class definition ===
# This class represents the game logic and manages the game state.
# It includes methods to switch players, get the current agent and play the game.
# Feel free to add parameters or adjust these functions as needed
# =========================
class Game:
  def __init__(self, board, agent1=None, agent2=None, size = 3):
    self.board = board # The game board instance
    self.agent1 = agent1
    self.agent2 = agent2
    self.current_player = 1
    self.size = size # Dont know if we are going to do 4x4 - I haven't seen much about 4x4. For now we're sticking with size of 3x3 (5x5 larger size later) to meet project requirement.
    return

  def switch_player(self):
    """Switch between player 1 and player 2"""
    if self.current_player == 1:
      self.current_player = 2
    elif self.current_player == 2:
      self.current_player = 1
    return

    # I created this to swap between players. If player 1 is 'X', then player 2 is 'O' for terminal command line interface.
    # if self.current_player == 'X':
    #   self.current_player = 'O'
    # elif self.current_player == 'O':
    #   self.current_player = 'X'

  def get_current_agent(self):
    """Get the current agent based on the current player"""
    if self.current_player == 1:
        return self.agent1
    elif self.current_player == 2:
        return self.agent2

  def play(self):
    print("Starting game...")
    # Main game loop
    while not self.board.is_game_over() and not self.board.is_full(): #while game not over and board is not full
      agent = self.get_current_agent()

      move = agent.get_action(self.board) # NOTE: for whoever is implimenting the agents here is where you would get all the moves
      if not self.board.is_valid_move(move):
          print(f"Invalid move by {agent}. Try again.")
          continue
      self.board.make_move(self.current_player,move)

      print(f"Player {self.get_current_agent()} made a move {move}.")

      self.switch_player()  # Switch to the next player

    # Game over handling
    winner = self.board.get_winner()
    if winner:
        print(f"Game Over! Player {winner} wins!")
    else:
        print("Game Over! It's a draw.")