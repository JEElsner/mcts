from mcts.mcts import MCTSAgent
from mcts.agents import FirstChoiceAgent
from mcts.game import Game

from . import TestState

import pytest

def test_init():
    agent = MCTSAgent()

@pytest.mark.parametrize("n_rounds", [3, 5, 51, 101, 1001])
def test_game(n_rounds):
    g = Game(TestState(n_rounds=n_rounds), {'A': MCTSAgent(), 'B': FirstChoiceAgent()})
    final_state = g.play()
    assert final_state.outcome.is_win
    assert final_state.outcome.winner == 'A'