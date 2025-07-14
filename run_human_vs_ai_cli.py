# run_human_vs_ai_cli.py
from visualization.cli_view import CLIView, select_agent
from agents.human_agent import HumanAgent
from agents.minimax_agent import MinimaxAgent


# 1) Define a trivial eval function:
#    +1 if the AI (’O’) has won, -1 if the human (’X’) has won, 0 otherwise.
def eval_fn(board):
    winner = board.get_winner()
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    return 0

if __name__ == '__main__':
    human = HumanAgent(mark='X')
    # 2) Instantiate MinimaxAgent with mark, eval_fn, and max_depth:
    #    max_depth=9 will fully search a 3×3 board.
    ai = MinimaxAgent(mark='O', eval_fn=eval_fn, max_depth=9)

    opp = select_agent('O')
    view = CLIView(agent1=HumanAgent('X'), agent2=opp)
    view.run()

