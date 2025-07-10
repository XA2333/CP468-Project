
# === Import libraries and modules ===
import time
from datetime import datetime
from game import Game, Board
from agents import MinimaxAgent, AlphaBetaAgent, ExpectiminimaxAgent, GeminiAgent, HumanAgent
from evaluation import Metrics, Logger
# ====================

# This is a placeholder for the main module of the game.
# Feel free to add parameters or adjust these functions as needed

# Global logger instance
game_logger = Logger("game_session.json")

# Simple evaluation function for AI agents
def simple_eval_function(board):
    """Simple evaluation function - returns random score for now"""
    if board.check_win('X'):
        return 100
    elif board.check_win('O'):
        return -100
    return 0 # if it's a draw

def get_agent(agent_type: str, mark: str, max_depth: int = 6):
    """
    Dynamically create an agent based on type.

    Args:
        agent_type (str): Type of agent ('human', 'minimax', 'alphabeta', 'expectiminimax', 'gemini')

    Returns:
        Agent instance or None if invalid type
    """
    if not agent_type:
        return None

    agent_type = agent_type.lower()

    AVAILABLE_AGENTS  = {
        'minimax': MinimaxAgent,
        'alphabeta': AlphaBetaAgent,
        'expectiminimax': ExpectiminimaxAgent,
        'gemini': GeminiAgent,
        'human': HumanAgent
    }

    if agent_type not in AVAILABLE_AGENTS :
        print(f"Unknown agent type: {agent_type}")
        return None

    # Create agent with appropriate parameters
    if agent_type in ['minimax', 'alphabeta', 'expectiminimax']:
        return AVAILABLE_AGENTS [agent_type](
            eval_fn=simple_eval_function,
            max_depth=max_depth,
            mark=mark
        )
    else:
        return AVAILABLE_AGENTS [agent_type](mark=mark)

# Game functions
def play_one_match(agent1_type: str, agent2_type: str, board_size: int = 3, max_depth: int = 6, enable_logging: bool = True):
    # Play a single match using appropriate method based on agent types
    print(f"\nGame: {agent1_type.upper()} (X) vs {agent2_type.upper()} (O)")
    print(f"Board: {board_size}x{board_size}, Max depth: {max_depth}")

    # Create agents
    agent1 = get_agent(agent1_type, 'X', max_depth)
    agent2 = get_agent(agent2_type, 'O', max_depth)

    if not agent1 or not agent2:
        print("Error: Could not initialize agents.")
        return None

    # Always use Game.play() for human players to show board progression
    if agent1_type == 'human' or agent2_type == 'human':
        board = Board(size=board_size)
        game = Game(board, agent1, agent2)

        start_time = time.time()
        game.play()
        end_time = time.time()

        # Extract results manually
        winner = game.board.get_winner() or 'Draw'
        execution_time = end_time - start_time
        agent1_nodes = getattr(agent1, 'nodes_expanded', 0)
        agent2_nodes = getattr(agent2, 'nodes_expanded', 0)
        total_moves = game.board.total_move

        result = {
            'winner': winner,
            'elapsed_sec': execution_time,
            'nodes_x': agent1_nodes,
            'nodes_o': agent2_nodes,
            'total_moves': total_moves
        }
    else:
        # Use Metrics.run_match()
        metrics = Metrics()
        result = metrics.run_match(agent1, agent2, board_size)

    # Extract results from metrics format
    winner = result['winner']
    execution_time = result['elapsed_sec']
    agent1_nodes = result['nodes_x']
    agent2_nodes = result['nodes_o']
    total_moves = result.get('total_moves', 0)

    # Convert winner
    if winner == 'X':
        winner_display = agent1_type
    elif winner == 'O':
        winner_display = agent2_type
    else:
        winner_display = winner  # 'Draw'

    # Print performance summary
    print(f"\nResults:")
    print(f"  Winner: {winner_display}")
    print(f"  Moves: {total_moves}")
    print(f"  Time: {execution_time:.4f}s")

    # Only show node counts for AI search agents
    search_agents = ['minimax', 'alphabeta', 'expectiminimax']

    if agent1_type in search_agents:
        print(f"  {agent1_type.upper()} nodes: {agent1_nodes}")
    else:
        print(f"  {agent1_type.upper()}: No node evaluation")

    if agent2_type in search_agents:
        print(f"  {agent2_type.upper()} nodes: {agent2_nodes}")
    else:
        print(f"  {agent2_type.upper()}: No node evaluation")

    # Log results if enabled
    if enable_logging:
        game_logger.log_game(
            agent1_type=agent1_type,
            agent2_type=agent2_type,
            winner=winner,
            total_moves=total_moves,
            execution_time=execution_time,
            board_size=board_size,
            agent1_nodes=agent1_nodes,
            agent2_nodes=agent2_nodes,
            additional_data={'max_depth': max_depth}
        )

    return {
        'agent1_type': agent1_type,
        'agent2_type': agent2_type,
        'winner': winner,
        'total_moves': total_moves,
        'execution_time': execution_time,
        'agent1_nodes': agent1_nodes,
        'agent2_nodes': agent2_nodes
    }

def run_performance_comparison():
    # Run performance comparison using Metrics.run_series()
    print("\nPerformance comparison: Minimax vs Alpha-Beta ")

    # Clear previous session data
    game_logger.clear()

    games = 10
    print(f"Running {games} games...")

    # Use Metrics.run_series() for structured testing
    metrics = Metrics()

    try:
        metrics.run_series(
            agent_cls_x=MinimaxAgent,
            agent_cls_o=AlphaBetaAgent,
            games=games,
            board_size=3,
            eval_fn=simple_eval_function,
            max_depth=6
        )

        # Display results using Metrics methods
        print(f"\nPerformance Results ")
        print(f"Total time: {metrics.get_execution_time():.4f}s")
        print(f"Avg time per game: {metrics.get_execution_time()/games:.4f}s")

        nodes_expanded = metrics.get_nodes_evaluated()
        print(f"Nodes - X: {nodes_expanded['X']}, O: {nodes_expanded['O']}")

        success_rates = metrics.get_success_rate()
        print(f"Win rates - X: {success_rates['X']*100:.1f}%, O: {success_rates['O']*100:.1f}%, Draw: {success_rates['Draw']*100:.1f}%")

        # Log each individual game result
        for i, record in enumerate(metrics.records):
            game_logger.log_game(
                agent1_type='minimax' if i % 2 == 0 else 'alphabeta',
                agent2_type='alphabeta' if i % 2 == 0 else 'minimax',
                winner=record['winner'],
                total_moves=record.get('total_moves', 0),
                execution_time=record['elapsed_sec'],
                board_size=3,
                agent1_nodes=record['nodes_x'] if i % 2 == 0 else record['nodes_o'],
                agent2_nodes=record['nodes_o'] if i % 2 == 0 else record['nodes_x'],
                additional_data={'max_depth': 6}
            )

        # Log summary
        game_logger.log({
            'comparison_type': 'Minimax vs Alpha-Beta',
            'total_games': len(metrics.records),
            'total_execution_time': metrics.get_execution_time(),
            'average_execution_time': metrics.get_execution_time() / len(metrics.records),
            'nodes_expanded': nodes_expanded ,
            'success_rates': success_rates,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error during performance comparison: {e}")
        print("Falling back to individual game method...")

        # Fallback to individual games
        for i in range(games):
            if i % 2 == 0:
                print(f"\nGame {i+1}: Minimax (X) vs Alpha-Beta (O)")
                play_one_match('minimax', 'alphabeta', 3, 6)
            else:
                print(f"\nGame {i+1}: Alpha-Beta (X) vs Minimax (O)")
                play_one_match('alphabeta', 'minimax', 3, 6)

def run_series_evaluation():
    # Run series evaluation using Metrics.run_series()
    print("\nSeries Evaluation ")

    valid_agents = ['minimax', 'alphabeta', 'expectiminimax', 'gemini', 'human']
    print(f"Available agents: {', '.join(valid_agents)}")

    agent1_type = input("Enter agent 1 type: ").strip().lower()
    agent2_type = input("Enter agent 2 type: ").strip().lower()

    if agent1_type not in valid_agents or agent2_type not in valid_agents:
        print("Invalid agent type. Please use one of:", valid_agents)
        return

    games = int(input("Enter number of games (default 10): ") or "10")

    print(f"\nRunning {games} games: {agent1_type.upper()} vs {agent2_type.upper()}")

    # Check if human player is involved
    has_human = agent1_type == 'human' or agent2_type == 'human'

    if has_human:
        print("\nHuman player detected - using visual game mode with board display")
        # Use individual games with board display for human players
        for i in range(games):
            if i % 2 == 0:
                print(f"\n Game {i+1}: {agent1_type.upper()} (X) vs {agent2_type.upper()} (O) ")
                play_one_match(agent1_type, agent2_type, 3, 6)
            else:
                print(f"\n Game {i+1}: {agent2_type.upper()} (X) vs {agent1_type.upper()} (O) ")
                play_one_match(agent2_type, agent1_type, 3, 6)
        return

    # For AI-only games, use Metrics.run_series() method
    AVAILABLE_AGENTS  = {
        'minimax': MinimaxAgent,
        'alphabeta': AlphaBetaAgent,
        'expectiminimax': ExpectiminimaxAgent,
        'gemini': GeminiAgent,
        'human': HumanAgent
    }

    # Use Metrics.run_series() for structured evaluation
    metrics = Metrics()

    try:
        # Prepare kwargs for AI agents
        agent_kwargs = {}
        if agent1_type in ['minimax', 'alphabeta', 'expectiminimax'] or agent2_type in ['minimax', 'alphabeta', 'expectiminimax']:
            agent_kwargs = {
                'eval_fn': simple_eval_function,
                'max_depth': 6
            }

        # Run series using Metrics
        metrics.run_series(
            agent_cls_x=AVAILABLE_AGENTS [agent1_type],
            agent_cls_o=AVAILABLE_AGENTS [agent2_type],
            games=games,
            board_size=3,
            **agent_kwargs
        )

        # Display results
        print(f"\n Series Results ")
        print(f"Total time: {metrics.get_execution_time():.4f}s")
        print(f"Avg time per game: {metrics.get_execution_time()/games:.4f}s")

        nodes_expanded = metrics.get_nodes_evaluated()
        print(f"Nodes - X: {nodes_expanded['X']}, O: {nodes_expanded['O']}")

        success_rates = metrics.get_success_rate()
        print(f"Win rates - X: {success_rates['X']*100:.1f}%, O: {success_rates['O']*100:.1f}%, Draw: {success_rates['Draw']*100:.1f}%")

        # Log each individual game result
        for i, record in enumerate(metrics.records):
            game_logger.log_game(
                agent1_type=agent1_type if i % 2 == 0 else agent2_type,
                agent2_type=agent2_type if i % 2 == 0 else agent1_type,
                winner=record['winner'],
                total_moves=record.get('total_moves', 0),
                execution_time=record['elapsed_sec'],
                board_size=3,
                agent1_nodes=record['nodes_x'] if i % 2 == 0 else record['nodes_o'],
                agent2_nodes=record['nodes_o'] if i % 2 == 0 else record['nodes_x'],
                additional_data={'max_depth': 6}
            )

        # Log summary
        game_logger.log({
            'series_type': f'{agent1_type} vs {agent2_type}',
            'total_games': len(metrics.records),
            'total_execution_time': metrics.get_execution_time(),
            'average_execution_time': metrics.get_execution_time() / len(metrics.records),
            'nodes_expanded': nodes_expanded,
            'success_rates': success_rates,
            'board_size': 3,
            'max_depth': 6,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error during series evaluation: {e}")
        print("Falling back to individual game method")

        # Fallback to individual games
        for i in range(games):
            if i % 2 == 0:
                print(f"\nGame {i+1}: {agent1_type.upper()} (X) vs {agent2_type.upper()} (O)")
                play_one_match(agent1_type, agent2_type, 3, 6)
            else:
                print(f"\nGame {i+1}: {agent2_type.upper()} (X) vs {agent1_type.upper()} (O)")
                play_one_match(agent2_type, agent1_type, 3, 6)

def run_user_match():
    # Run a single match with user-specified agents
    print("\nSingle match setup ")

    valid_agents = ['minimax', 'alphabeta', 'expectiminimax', 'gemini', 'human']
    print(f"Available agents: {', '.join(valid_agents)}")

    agent1_type = input("Enter agent 1 type (X): ").strip().lower()
    agent2_type = input("Enter agent 2 type (O): ").strip().lower()

    if agent1_type not in valid_agents or agent2_type not in valid_agents:
        print("Invalid agent type. Please use one of:", valid_agents)
        return

    # Ask if user wants to show board progression
    show_board = input("Show board during game? (y/n, default y): ").strip().lower() == 'y'

    if show_board:
        # Use Game.play() for visual gameplay
        agent1 = get_agent(agent1_type, 'X', 6)
        agent2 = get_agent(agent2_type, 'O', 6)

        if agent1 and agent2:
            board = Board(size=3)
            game = Game(board, agent1, agent2)
            game.play()
    else:
        # Use regular play_one_match
        play_one_match(agent1_type, agent2_type, 3, 6)

#  Menu Functions
def display_evaluation_options():
    # Display evaluation menu
    while True:
        print("\nEvaluation menu ")
        print("1. Performance comparison (Minimax vs Alpha-Beta - for testing)")
        print("2. Series evaluation (custom agents)")
        print("3. Export performance comparison to file")
        print("4. Save all logged results to file")
        print("5. Back to main menu")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            run_performance_comparison()
        elif choice == '2':
            run_series_evaluation()
        elif choice == '3':
            game_logger.export_performance_comparison("overall_performance_comparison.json")
        elif choice == '4':
            format_choice = input("Save as csv or json: ").strip().lower()
            if format_choice == 'csv':
                game_logger.save_to_file(format='csv')
            else:
                game_logger.save_to_file(format='json')
        elif choice == '5':
            return
        elif choice == '6':
            exit()
        else:
            print("Invalid choice, please try again.")

def main():
    # Main entry point
    while True:
        print("Tic Tac Toe game")
        print("1. Run a single match")
        print("2. Evaluation menu")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            run_user_match()
        elif choice == '2':
            display_evaluation_options()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
