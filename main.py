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
    import random
    return random.randint(-10, 10)

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
    
    if agent_type == 'alphabeta':
        return AlphaBetaAgent(eval_fn=simple_eval_function, max_depth=3)
    elif agent_type == 'expectiminimax':
        return ExpectiminimaxAgent(eval_fn=simple_eval_function, max_depth=3)
    elif agent_type in AVAILABLE_AGENTS:
        # For human, minimax, gemini agents 
        return AVAILABLE_AGENTS[agent_type]()
    else:
        print(f"Unknown agent type: {agent_type}")
        return None

def main():
    # test the game with a human and alphabeta agent
    agent1 = get_agent('human')
    agent2 = get_agent('alphabeta')
    board = Board()
    # Uncomment the following lines to test with other agents 
    game = Game(board, agent1=agent1, agent2=agent2)
    game.play()


if __name__ == "__main__":
    main()
