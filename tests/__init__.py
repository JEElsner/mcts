from itertools import cycle

from typing import Any, Collection

from collections import Counter

from copy import deepcopy

from mcts.state import AbstractState, Outcome
from mcts import state

class TestState(AbstractState):
    """A simple test game state.

    Players take turns choosing numbers. The player who has chosen the same
    number the most number of times after a set number of rounds wins. If
    multiple players choose the same number the same number of times, there is a
    tie.
    
    Attributes:
        rounds:
            A list of rounds. Each round comprises a tuple of the player and their choice of number.
        n_rounds:
            The number of rounds that will be played.
        players:
            A cycle of the players in the game.
        moves:
            The possible moves any player can make on their turn.
        _player: The current player whose turn it is.
    """

    def __init__(self, rounds=list(), n_rounds=4, players=['A', 'B'], moves=[1, 2, 3]):
        self.rounds = rounds
        self.n_rounds = n_rounds
        self.players = players
        self.moves = moves

    @property
    def outcome(self) -> Outcome:
        if len(self.rounds) < self.n_rounds:
            return state.Undecided
        
        counts = Counter(self.rounds)
        (t1, c1), (t2, c2) = counts.most_common(2)
        if c1 == c2 and t1[0] != t2[0]:
            return state.Tie
        else:
            return state.Win(t1[0])

    @property
    def current_player(self) -> int:
        return self.players[0]

    def possible_moves(self) -> Collection[Any]:
        return self.moves.copy()

    def next_move(self, player, move) -> AbstractState:
        if player != self.current_player:
            raise ValueError("Cannot make a move if not the current player.")
        
        if move not in self.possible_moves():
            raise ValueError("Illegal move!")
        
        rounds = deepcopy(self.rounds)
        rounds.append((player, move))

        return TestState(
            rounds=rounds,
            n_rounds=self.n_rounds,
            players=self.players[1:] + [self.players[0]],
            moves=self.moves
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TestState):
            return False
        
        return self.rounds == value.rounds \
            and self.players == value.players \
            and self.n_rounds == value.n_rounds \
            and self.moves == value.moves

    def __str__(self) -> str:
        return str(self.rounds) + f" Turn: {self.current_player}"
    
    def __repr__(self) -> str:
        n_rounds=self.n_rounds
        moves=self.moves
        players = self.players
        return f"TestState({self.rounds}, {n_rounds=}, {players=}, {moves=})"
