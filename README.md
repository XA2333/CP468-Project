
# Tic Tac Toe
This project is a multi-agent Tic-Tac-Toe game developed for **Artificial Intelligence** class showcasing probabilistic AI Algorithm like **Minimax**, **Alpha-Beta Pruning** and **Expectiminimax** with integration of **Gemini API** to simulate external LLM-based agents.

## Folder structure
| Filename / Folder            | Description                                                  |
|-----------------------------|--------------------------------------------------------------|
| ``main.py``             | Main entry point for launching the game                      |
| ``.gitignore``             | Ignores when tracking changes and committing code                      |
| ``requirements.txt``       | List of dependencies to install                              |
| ``README.md``               | Project overview, setup instructions, and documentation       |
| ``run_human_vs_ai_cli.py``   | Used to run the CLI       |
| ``run_human_vs_ai_gui.py``   | Used to run the GUI       |
| **config/**                   | Configuration files and API key setup           |
| └── `gemini_settings.json`              | JSON config for Gemini API key                      |
| **game/**                   | Contains core game logic, rules, and board display           |
| └── `__init__.py`         | Allows importing game components      |
| └── `board.py`              | Checks for valid moves, makes moves, checks for a win and resets the board                      |
| └── `game.py`              | Manages game loop, agent switching, and game progression                          |
| **agents/**                 | All agent implementations                       |
| └── `__init__.py`         | Allows importing AI agent modules                 |
| └── `minimax_agent.py`      | Minimax agent                                 |
| └── `alpha_beta_agent.py`   | Alpha-Beta pruning agent                      |
| └── `expectiminimax_agent.py` | Expectiminimax agent                          |
| └── `gemini_agent.py`       | Google Gemini API agent                                |
| └── `human_agent.py`       | Allows a human player to make moves in a game                               |
| **evaluation/**             | Tools for benchmarking and performance evaluation            |
| └── `__init__.py`         | 	Enables benchmarking tools as a package                 |
| └── `metrics.py`            | Tracks execution time, number of nodes evaluated and success rate of the agents                  |
| └── `results_logger.py`     | Logs and stores results for visualization                                             |
| **assets/**                 | All generated visuals, game trees and screenshots           |
| **visualization/**                 | Tools for visualizing the game           |
| └── `cli_view.py`         | Console-based interface      |
| └── `gui_view.py`              | Graphical interface              |
| └── `tree_diagram.py`              | Highlights pruned branches in Alpha-Beta Pruning                    |
| **docs/**                   | Final project report and presentation poster                   |
| └── `CP468-PT-Group8.pptx`            | Final presentation                                     |
| └── `CP468-PT-Group8.pdf`            | Project report                                    |
## Agents used
| Agent | Description |
|---------------|---------------------------------------------------------------|
| **Minimax** | Explores all possible moves to select optimal strategy |
| **Alpha-Beta**| Minimax with pruning to skip irrelevant branches |
| **Expectiminimax**| Handles uncertainty by combining Minimax with probabilistic chance nodes|
| **Gemini** | Integrates Google Gemini LLM to make move decisions via API interaction|
| **Human** | Allows player to make moves through console-based input |

## How to run
### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Start game
```bash
python main.py
```

## References
- Artificial Intelligence: A Modern Approach by Stuart Russell and Peter Norvig
- Introduction to Algorithms by Thomas H. Cormen et al.
- Gemini API Documentation
- Python: **pygame**, **matplotlib**

## Collaborators
[@Isaac Sigethy](https://github.com/Isaac-Sigethy) [@Mahmoud Yousif](https://github.com/Diorski) [@Nguyen Hai Trung Pham](https://github.com/TristanPham2375) [@Shankar Parat](https://github.com/shankarparat) [@Thu Mai](https://github.com/mnathuw) [@Wentao Ma](https://github.com/XA2333) [@Xinping Wang](https://github.com/frankxpw) [@Xinyu Luo](https://github.com/luoxinyu538)

## Future improvements
N/A
