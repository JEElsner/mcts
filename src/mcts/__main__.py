from .game import Game
from .ttt import TicTacToeState
from .agents import ConsoleAgent
from .mcts import MCTSAgent

def main():
    g = Game(TicTacToeState(), {"X": ConsoleAgent(), "O": MCTSAgent()})
    g.play()

print()
main()