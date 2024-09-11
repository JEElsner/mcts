from random import Random

from mcts.mcts import MCTSAgent
from mcts.agents import FirstChoiceAgent
from mcts.game import Game

from . import TestState, MockRng

import pytest

def test_init():
    agent = MCTSAgent()

@pytest.mark.parametrize("n_rounds", [3, 5, 51, 101, 1001])
def test_game_deterministic(n_rounds):
    g = Game(TestState(n_rounds=n_rounds), {'A': MCTSAgent(rng=MockRng()), 'B': FirstChoiceAgent()})
    final_state = g.play()
    assert final_state.outcome.is_win
    assert final_state.outcome.winner == 'A'
    

@pytest.mark.parametrize("n_rounds", [3, 5, 51, 101])
def test_game(n_rounds):
    g = Game(TestState(n_rounds=n_rounds), {'A': MCTSAgent(rng=Random(42)), 'B': FirstChoiceAgent()})
    final_state = g.play()
    assert final_state.outcome.is_win
    assert final_state.outcome.winner == 'A'