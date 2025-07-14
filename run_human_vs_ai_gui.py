# run_human_vs_ai_gui.py
from visualization.gui_view import GUIView, select_agent
from agents.human_agent import HumanAgent
from agents.alpha_beta_agent import AlphaBetaAgent

def eval_fn(board):
    winner = board.get_winner()
    if winner == 'O': return 1
    if winner == 'X': return -1
    return 0

if __name__ == '__main__':
    human = HumanAgent(mark='X')
    ai    = AlphaBetaAgent(
                eval_fn=eval_fn,   # 1) your evaluation function
                max_depth=9,       # 2) full 3×3 search
                mark='O'           # 3) O plays second
            )
    opp = select_agent('O')
    view = GUIView(agent1=HumanAgent('X'), agent2=opp)
    view.run()

