# === Import libraries and modules ===
# Place all your import statements here
# =========================================

# === Game class definition ===
# This class represents the game logic and manages the game state.
# It includes methods to switch players, get the current agent and play the game.
# Feel free to add parameters or adjust these functions as needed
# =========================
class Game:
  def __init__(self, board, agent1, agent2):
    self.board = board # The game board instance
    self.agent1 = agent1
    self.agent2 = agent2
    self.current_player = 'X'
    self.size = board.size

  def switch_player(self):
    #"""Switch between player 1 and player 2"""
    # if self.current_player == 1:
    #   self.current_player = 2
    # elif self.current_player == 2:
    #   self.current_player = 1
    # return
    """Switch between 'X' and 'O' players"""
    if self.current_player == 'X':
      self.current_player = 'O'
    else:
      self.current_player = 'X'

  def get_current_agent(self):
    """Get the current agent based on the current player"""
    if self.current_player == self.agent1.mark:
      return self.agent1
    elif self.current_player == self.agent2.mark:
      return self.agent2
    else:
      raise ValueError(f"No agent found for current player mark: {self.current_player}")

  def play(self):
    print("Starting game...")

    # Main game loop
    while not self.board.is_game_over(): #while game not over
      agent = self.get_current_agent()
      print(f"\n{self.board}") # Display board before current player's move
      print(f"It's player {self.current_player}'s turn.")

      # Agents should return a (row, col) tuple
      move = agent.get_action(self.board) # NOTE: for whoever is implimenting the agents here is where you would get all the moves
      row, col = move

      if not self.board.make_move(row, col, self.current_player):
        # If an AI agent makes an invalid move, it's a bug in the AI.
        # For a human agent, it prompts them to retry.
        continue

      print(f"Player {self.current_player} made a move: {move}.")

      if self.board.is_game_over():
        break

      self.switch_player()  # Switch to the next player

    # Game over handling
    print(f"\n{self.board}")
    winner = self.board.get_winner()
    if winner:
      print(f"Game Over! Player {winner} wins!")
    else:
      print("It's a draw.")
