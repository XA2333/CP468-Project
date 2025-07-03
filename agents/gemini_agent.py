"""
Gemini Agent: (still need board.py to integrate this agent)
This agent uses Gemini language model to choose moves in Tic Tac Toe by prompting the model with the current board state and valid actions.

Features:
- Uses Gemini API to generate a move (row,col)
- Automatically falls back to random moves if API fails or key is missing
- API key stored in .env file or config/gemini_settings.json
- Coverts game state into a text prompt
- Trying to use different prompts to improve performance by providing more context like:
1. If there is a winning move, take it immediately
2. If the opponent has a winning move, play third spot to block their win
3. Follow opening theory: must take center first, then corners, then edges (always end up with a win or draw)

Dependencies:
- google-generativeai: Google Gemini API SDK (gemini-1.5-flash-latest)
- python-dotenv: to load api key from .env file

Setup:
1. Install dependencies (add dotenv to requirements.txt):
  pip install -r requirements.txt
2. Configure your API key in one of the following ways:
  a) Create a '.env' file in the project's root directory:
    GEMINI_API_KEY=your_api_key_here
  b) Create a JSON configuration file at 'config/gemini_config.json':
    { "GEMINI_API_KEY": "your_api_key_here" }

Date: 2025-07-03
Version: 1.0
"""
import json
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiAgent:
  def __init__(self, mark):
    # Initialize the Gemini API agent.
    self.mark = mark
    # self.opponent_mark = 'O' if mark == 'X' else 'X'
    # self.api_configured = False

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Fallback to JSON config if .env or environment variable is not set
    if not api_key:
      try:
        with open("config/gemini_config.json", "r") as f:
          config = json.load(f)
          api_key = config.get("GEMINI_API_KEY") or config.get("api_key")
      except (FileNotFoundError, json.JSONDecodeError):
        pass

    if not api_key:
      print(f"Gemini cannot be found. Agent will make random moves.")
      self.api_configured = False
    else:
      try:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest") # the latest free model
        self.api_configured = True
        print(f"Gemini API configured successfully.")
      except Exception as e:
        # Catching any exception during API configuration
        print(f"Error configuring Gemini API: {e}. Agent will make random moves.")
        self.api_configured = False

  def get_action(self, board):
    # Get the best move by querying Gemini API
    valid_moves = board.get_valid_moves()

    # If there is only one valid move, return it immediately
    if len(valid_moves) == 1:
      return valid_moves[0]

    # If Gemini API is not configured, return a random move
    if not self.api_configured:
      return random.choice(valid_moves)

    # Main API call logic
    try:
      board_str = self._board_to_string(board)
      # To improve performance, we can try different prompts
      prompt = f"""
      You are playing Tic-Tac-Toe.
      Your mark is '{self.mark}'.
      The opponent's mark: '{self.opponent_mark}'.

      Current board ({board.size}x{board.size}):
      {board_str}

      Valid moves: {valid_moves}

      Only make a move from the list. Your response must be in the format: row,col
      Example: 1,2
      """
      response = self.model.generate_content(prompt)
      if not response or not response.text:
          raise ValueError("Gemini API returned an empty or invalid response.")

      # Parse the response text to extract the move
      response_text = response.text.strip()
      row_str, col_str = response_text.split(',')

      # For example, if the response is "1,2", we convert it to a tuple (1, 2)
      move = (int(row_str.strip()), int(col_str.strip()))

      # Validate the move
      if move in valid_moves:
          print(f"Gemini Agent chose move: {move}")
          return move
      else:
          print(f"Gemini Agent returned an invalid move: {move}. Falling back to random move.")
          return random.choice(valid_moves)

    except Exception as e:
      print(f"Error during Gemini API call: {e}. Falling back to random move.")
      return random.choice(valid_moves)

  def _board_to_string(self, board):
    # Converts the board state to a string representation.
    board_str = ""
    for row in range(board.size):
      for col in range(board.size):
        cell = board.get_state(row, col)
        if cell is None:
          board_str += ". "
        else:
          board_str += f"{cell} "
      board_str += "\n"
    return board_str.strip()



