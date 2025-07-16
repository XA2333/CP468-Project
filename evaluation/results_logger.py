# === Import libraries and modules ===
import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
# =========================================

# === Results logger ===
# This class is responsible for logging the results of the game.
# It will store the results in a list and provide methods to log, retrieve, and clear the logs.
# It supports multiple output formats: JSON, CSV, and console display.
# =========================

class Logger:
    def __init__(self, log_file: str = "game_results.json"):
        """
        Initialize the Logger with optional file output.

        Args:
            log_file (str): Name of the file to save logs to
        """
        self.logs = []
        self.log_file = log_file
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_folder = "results"

        # Create results folder if it doesn't exist
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)

    def log(self, game_result: Dict[str, Any]):
        """
        Log a single game result.

        Args:
            game_result (Dict): Dictionary containing game information
                Expected keys:
                - agent1_type: Type of agent 1 (e.g., 'minimax', 'alphabeta')
                - agent2_type: Type of agent 2
                - winner: Winner of the game ('X', 'O', or 'Draw')
                - total_moves: Total number of moves in the game
                - execution_time: Total game execution time
                - board_size: Size of the game board
                - agent1_nodes_evaluated: Nodes evaluated by agent 1 (if applicable)
                - agent2_nodes_evaluated: Nodes evaluated by agent 2 (if applicable)
                - timestamp: When the game was played
        """
        # Add session ID and timestamp if not provided
        if 'session_id' not in game_result:
            game_result['session_id'] = self.session_id
        if 'timestamp' not in game_result:
            game_result['timestamp'] = datetime.now().isoformat()

        self.logs.append(game_result)

    def log_game(self, agent1_type: str, agent2_type: str, winner: str,
                 total_moves: int, execution_time: float, board_size: int = 3,
                 agent1_nodes: Optional[int] = None, agent2_nodes: Optional[int] = None,
                 additional_data: Optional[Dict] = None):
        """
        Convenience method to log game results with individual parameters.

        Args:
            agent1_type (str): Type of agent 1
            agent2_type (str): Type of agent 2
            winner (str): Winner of the game ('X', 'O', or 'Draw')
            total_moves (int): Total number of moves
            execution_time (float): Game execution time in seconds
            board_size (int): Size of the game board
            agent1_nodes (int, optional): Nodes evaluated by agent 1
            agent2_nodes (int, optional): Nodes evaluated by agent 2
            additional_data (Dict, optional): Any additional data to log
        """
        game_result = {
            'agent1_type': agent1_type,
            'agent2_type': agent2_type,
            'winner': winner,
            'total_moves': total_moves,
            'execution_time': execution_time,
            'board_size': board_size,
            'agent1_nodes_evaluated': agent1_nodes,
            'agent2_nodes_evaluated': agent2_nodes
        }

        if additional_data:
            game_result.update(additional_data)

        self.log(game_result)

    def get_logs(self) -> List[Dict[str, Any]]:
        """
        Get all logged results.

        Returns:
            List[Dict]: List of all game results
        """
        return self.logs.copy()

    def get_logs_by_agent(self, agent_type: str) -> List[Dict[str, Any]]:
        """
        Get logs filtered by specific agent type.

        Args:
            agent_type (str): Type of agent to filter by

        Returns:
            List[Dict]: Filtered game results
        """
        return [log for log in self.logs
                if log.get('agent1_type') == agent_type or log.get('agent2_type') == agent_type]

    def get_performance_summary(self, agent_type: str) -> Dict[str, Any]:
        """
        Get performance summary for a specific agent type.

        Args:
            agent_type (str): Type of agent to analyze

        Returns:
            Dict: Performance summary including win rate, avg execution time, etc.
        """
        agent_logs = self.get_logs_by_agent(agent_type)

        if not agent_logs:
            return {'error': f'No logs found for agent type: {agent_type}'}

        total_games = len(agent_logs)
        wins = sum(1 for log in agent_logs
                  if (log.get('agent1_type') == agent_type and log.get('winner') == 'X') or
                     (log.get('agent2_type') == agent_type and log.get('winner') == 'O'))
        draws = sum(1 for log in agent_logs if log.get('winner') == 'Draw')

        avg_execution_time = sum(log.get('execution_time', 0) for log in agent_logs) / total_games
        avg_moves = sum(log.get('total_moves', 0) for log in agent_logs) / total_games

        # Calculate average nodes evaluated if available
        nodes_data = []
        for log in agent_logs:
            if log.get('agent1_type') == agent_type and log.get('agent1_nodes_evaluated'):
                nodes_data.append(log.get('agent1_nodes_evaluated'))
            elif log.get('agent2_type') == agent_type and log.get('agent2_nodes_evaluated'):
                nodes_data.append(log.get('agent2_nodes_evaluated'))

        avg_nodes = sum(nodes_data) / len(nodes_data) if nodes_data else None

        return {
            'agent_type': agent_type,
            'total_games': total_games,
            'wins': wins,
            'draws': draws,
            'losses': total_games - wins - draws,
            'win_rate': wins / total_games * 100,
            'draw_rate': draws / total_games * 100,
            'avg_execution_time': avg_execution_time,
            'avg_moves_per_game': avg_moves,
            'avg_nodes_evaluated': avg_nodes
        }

    def clear(self):
        """Clear all logged results."""
        self.logs.clear()

    def save_to_file(self, filename: Optional[str] = None, format: str = 'json'):
        """
        Save logs to file in specified format.

        Args:
            filename (str, optional): Custom filename, uses default if None
            format (str): File format ('json' or 'csv')
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if format == 'json':
                filename = f"game_results_{timestamp}.json"
            elif format == 'csv':
                filename = f"game_results_{timestamp}.csv"

        # Create full path in results folder
        filepath = os.path.join(self.results_folder, filename)

        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, indent=2, ensure_ascii=False)
        elif format == 'csv':
            if self.logs:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.logs[0].keys())
                    writer.writeheader()
                    writer.writerows(self.logs)

        print(f"Results saved to {filepath}")

    def load_from_file(self, filename: str):
        """
        Load logs from a JSON file.

        Args:
            filename (str): Name of the file to load from
        """
        # Check if filename includes path, if not, assume it's in results folder
        if not os.path.dirname(filename):
            filepath = os.path.join(self.results_folder, filename)
        else:
            filepath = filename

        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.logs = json.load(f)
            print(f"Loaded {len(self.logs)} results from {filepath}")
        else:
            print(f"File {filepath} not found")

    def print_summary(self):
        """Print a summary of all logged results."""
        if not self.logs:
            print("No game results logged yet.")
            return

        print(f"\n=== Game Results Summary ===")
        print(f"Total games played: {len(self.logs)}")
        print(f"Session ID: {self.session_id}")

        # Count results by agent type
        agent_types = set()
        for log in self.logs:
            agent_types.add(log.get('agent1_type', 'unknown'))
            agent_types.add(log.get('agent2_type', 'unknown'))

        for agent_type in sorted(agent_types):
            if agent_type != 'unknown':
                summary = self.get_performance_summary(agent_type)
                print(f"\n{agent_type.upper()} Performance:")
                print(f"  Games played: {summary['total_games']}")
                print(f"  Win rate: {summary['win_rate']:.1f}%")
                print(f"  Draw rate: {summary['draw_rate']:.1f}%")
                print(f"  Avg execution time: {summary['avg_execution_time']:.3f}s")
                if summary['avg_nodes_evaluated']:
                    print(f"  Avg nodes evaluated: {summary['avg_nodes_evaluated']:.0f}")

    def print_detailed_results(self, limit: Optional[int] = None):
        """
        Print detailed results of recent games.

        Args:
            limit (int, optional): Number of recent games to show
        """
        if not self.logs:
            print("No game results to display.")
            return

        logs_to_show = self.logs[-limit:] if limit else self.logs

        print(f"\n=== Detailed Game Results ===")
        for i, log in enumerate(logs_to_show, 1):
            print(f"\nGame {i}:")
            print(f"  {log.get('agent1_type', 'Unknown')} (X) vs {log.get('agent2_type', 'Unknown')} (O)")
            print(f"  Winner: {log.get('winner', 'Unknown')}")
            print(f"  Moves: {log.get('total_moves', 'N/A')}")
            print(f"  Time: {log.get('execution_time', 0):.3f}s")
            if log.get('agent1_nodes_evaluated'):
                print(f"  {log.get('agent1_type')} nodes: {log.get('agent1_nodes_evaluated')}")
            if log.get('agent2_nodes_evaluated'):
                print(f"  {log.get('agent2_type')} nodes: {log.get('agent2_nodes_evaluated')}")

    def export_performance_comparison(self, filename: str = "performance_comparison.json"):
        """
        Export performance comparison of all agent types.

        Args:
            filename (str): Name of the file to export to
        """
        agent_types = set()
        for log in self.logs:
            agent_types.add(log.get('agent1_type', ''))
            agent_types.add(log.get('agent2_type', ''))

        agent_types.discard('')  # Remove empty strings

        # Generate performance comparison
        comparison = {}
        for agent_type in agent_types:
            summary = self.get_performance_summary(agent_type)
            if 'error' not in summary:
                comparison[agent_type] = summary


        # Create full path in results folder
        filepath = os.path.join(self.results_folder, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)

        print(f"Performance comparison exported to {filepath}")
        print(f"Exported data for {len(comparison)} agent types:")
        for agent_type, data in comparison.items():
            print(f"  - {agent_type}: {data['total_games']} games, {data['win_rate']:.1f}% win rate")



# === Test and Demo Code ===
# This section demonstrates the Logger functionality
if __name__ == "__main__":
    # Create a Logger instance
    logger = Logger("demo_results.json")

    print("=== Logger Demo Started ===")

    # Add some sample game results
    logger.log_game("minimax", "alphabeta", "X", 7, 0.125, 3, 150, 89)
    logger.log_game("alphabeta", "random", "O", 5, 0.087, 3, 45, None)
    logger.log_game("minimax", "random", "Draw", 9, 0.203, 3, 250, None)
    logger.log_game("alphabeta", "minimax", "X", 6, 0.156, 3, 78, 180)
    logger.log_game("random", "minimax", "O", 4, 0.034, 3, None, 95)

    print(f"\nAdded {len(logger.get_logs())} game results")

    # Display summary
    logger.print_summary()

    # Display detailed results (only show last 3)
    logger.print_detailed_results(limit=3)

    # Display specific agent performance
    print("\n=== Minimax Agent Performance Analysis ===")
    minimax_summary = logger.get_performance_summary("minimax")
    if 'error' not in minimax_summary:
        print(f"Total games: {minimax_summary['total_games']}")
        print(f"Win rate: {minimax_summary['win_rate']:.1f}%")
        print(f"Draw rate: {minimax_summary['draw_rate']:.1f}%")
        print(f"Average execution time: {minimax_summary['avg_execution_time']:.3f}s")
        if minimax_summary['avg_nodes_evaluated']:
            print(f"Average nodes evaluated: {minimax_summary['avg_nodes_evaluated']:.0f}")

    # Export performance comparison
    logger.export_performance_comparison("demo_performance.json")

    # Save results to files
    logger.save_to_file("demo_results.json", "json")
    logger.save_to_file("demo_results.csv", "csv")

    print("\n=== Logger Demo Completed ===")