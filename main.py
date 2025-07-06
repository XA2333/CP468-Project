# === Import libraries and modules ===
# Place all your import statements here
# ====================
from game import Game, Board
from agents import MinimaxAgent, AlphaBetaAgent, ExpectiminimaxAgent, GeminiAgent, HumanAgent
from evaluation import Metrics, Logger
from visualization import CLIView, GUIView, TreeDiagram


# This is a placeholder for the main module of the game.
# Feel free to add parameters or adjust these functions as needed

# Agent factory for dynamic agent creation
# usage example: agent = get_agent('minimax')
AVAILABLE_AGENTS = {
    'human': HumanAgent,
    'minimax': MinimaxAgent,
    'alphabeta': AlphaBetaAgent,
    'expectiminimax': ExpectiminimaxAgent,
    'gemini': GeminiAgent
}

# Simple evaluation function for AI agents
def simple_eval_function(state):
    """Simple evaluation function - returns random score for now"""
    board = state
    if board.check_win('X'):
        return 100
    if board.check_win('O'):
        return -100
    return 0 # if it's a draw

def get_agent(agent_type: str, mark: str, max_depth: int = 3):
    """
    Dynamically create an agent based on type.

    Args:
        agent_type (str): Type of agent ('human', 'minimax', 'alphabeta', 'expectiminimax', 'gemini')

    Returns:
        Agent instance or None if invalid type
    """
    if agent_type is None:
        return None

    agent_type = agent_type.lower()

    if agent_type == 'alphabeta':
        return AlphaBetaAgent(eval_fn=simple_eval_function, max_depth=6, mark=mark)
    elif agent_type == 'expectiminimax':
        return ExpectiminimaxAgent(eval_fn=simple_eval_function, max_depth=6, mark=mark)
    elif agent_type == 'minimax':
        return MinimaxAgent(eval_fn=simple_eval_function, max_depth=6, mark=mark)
    elif agent_type == 'human':
        return HumanAgent(mark=mark)
    elif agent_type == 'gemini':
        return GeminiAgent(mark=mark)
    else:
        print(f"Unknown agent type: {agent_type}")
        return None

def main():
    # test the game with a human and alphabeta agent
    board_size = 3
    # agent1 = get_agent('human')
    # agent2 = get_agent('alphabeta')
    # board = Board()
    board = Board(size=board_size)

    # Uncomment the following lines to test
    # # =========== Agent configuration ===========

    # # Example 1: Human (X) vs AlphaBeta (O)
    # agent1 = get_agent('human', 'X')
    # agent2 = get_agent('alphabeta', 'O', max_depth=6)

    # # Example 2: AlphaBeta (X) vs Gemini (O)
    # agent1 = get_agent('gemini', 'O')
    # agent2 = get_agent('alphabeta', 'X', max_depth=6)

    # # Example 3: Gemini (X) vs Human (O)
    # agent1 = get_agent('gemini', 'X')
    # agent2 = get_agent('human', 'O')

    # # Example 4: AlphaBeta (X) vs AlphaBeta (O)
    # agent1 = get_agent('alphabeta', 'X', max_depth=6)
    # agent2 = get_agent('alphabeta', 'O', max_depth=6)

    # Example 5: Human (X) vs Expectiminimax (0)
    agent1 = get_agent('human', 'X')
    agent2 = get_agent('expectiminimax', 'O', max_depth=6)

    # # Example 6: Human (X) vs Expectiminimax (O)
    # agent1 = get_agent('human', 'X')
    # agent2 = get_agent('expectiminimax', 'O', max_depth=6)

    # Validate agent creation
    if agent1 is None or agent2 is None:
        print("Error: Could not initialize agents. Exiting...")
        return

    # Create and play the game
    game = Game(board, agent1=agent1, agent2=agent2)
    game.play()


if __name__ == "__main__":
    main()
