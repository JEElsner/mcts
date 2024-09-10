from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Collection

class WinState:
    pass

class Undecided(WinState):
    def __bool__(self):
        return False
    
class Decided(WinState):
    def __bool__(self):
        return True

class Tie(Decided):
    pass

class Win(Decided):
    def __init__(self, winner):
        self.winner = winner

class AbstractState(metaclass=ABCMeta):
    @property
    @abstractmethod
    def winner(self) -> WinState:
        pass

    @property
    @abstractmethod
    def current_player(self) -> int:
        pass

    @abstractmethod
    def possible_moves(self) -> Collection[Any]:
        """The possible moves that can be made by the current player in this state."""
        pass

    @abstractmethod
    def next_move(self, player, move) -> AbstractState:
        """Get the next game state when the given player makes the selected move."""
        pass

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass