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

def get_agent(agent_type=None):
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
    if agent_type in AVAILABLE_AGENTS:
        return AVAILABLE_AGENTS[agent_type](Board()) #init agent and return
    else:
        print(f"Unknown agent type: {agent_type}")
        return None
    
def main():
    # test the game with a human and minmax agent
    agent1 = get_agent('human')
    agent2 = get_agent('minimax')
    board = Board()
    
    
    
    game = Game(board, agent1=agent1, agent2=agent2)
    game.play()


if __name__ == "__main__":
    main()
