
# === Import libraries and modules ===
from game import Game, Board
from agents import MinimaxAgent, AlphaBetaAgent, ExpectiminimaxAgent, GeminiAgent, HumanAgent
from visualization.tree_diagram import TreeDiagram

# Evaluation function


def simple_eval_fn(board):
    winner = board.get_winner()
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    return 0


# Map string to agent classes
AGENT_OPTIONS = {
    'alphabeta': AlphaBetaAgent,
    'minimax': MinimaxAgent,
    'expectiminimax': ExpectiminimaxAgent,
    'gemini': GeminiAgent,
    'human': HumanAgent
}


def get_agent_by_type(agent_type, mark, depth=4):
    cls = AGENT_OPTIONS.get(agent_type.lower())
    if cls is None:
        raise ValueError(f"Invalid agent type: {agent_type}")

    if agent_type in ['alphabeta', 'minimax', 'expectiminimax', 'gemini']:
        return cls(eval_fn=simple_eval_fn, max_depth=depth, mark=mark)
    else:
        return cls(mark=mark)


def main():
    print("\nChoose opponent for AlphaBetaAgent (X):")
    print("Options: minimax, alphabeta, expectiminimax, gemini, human")
    opponent_type = input("Enter agent type for Player O: ").strip().lower()

    try:
        agent1 = AlphaBetaAgent(eval_fn=simple_eval_fn, max_depth=4, mark='X')
        agent2 = get_agent_by_type(opponent_type, 'O', depth=4)
    except Exception as e:
        print(f"Error: {e}")
        return

    board = Board(size=3)
    game = Game(board, agent1, agent2)

    while not board.is_game_over():
        agent = game.get_current_agent()
        move = agent.get_action(board)
        board.make_move(*move, game.current_player)

        print(f"\nPlayer {game.current_player} played: {move}")
        print(board)

        if isinstance(agent, AlphaBetaAgent):
            print("Visualizing Alpha-Beta pruning tree for this move...")
            TreeDiagram(agent.last_search_tree).draw(
                title=f"Alpha-Beta Tree - Player {game.current_player}")

        if board.is_game_over():
            break

        game.switch_player()

    winner = board.get_winner()
    print(f"\nGame Over! Winner: {winner}" if winner else "\nGame Over! It's a draw.")


if __name__ == "__main__":
    main()
