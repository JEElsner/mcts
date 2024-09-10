from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Collection

class WinState(metaclass=ABCMeta):
    """
    Represents the outcome of a game.
     
    Namely whether there is a winner (and if so, who), a tie, or whether it is
    still undecided. An undecided game implies that further playout will decide
    the game, and a future state will have a winner or a tie.
    """

    @property
    @abstractmethod
    def is_decided(self):
        """Returns True IFF the game is decided, i.e. there is a winner or a tie."""
        return False
    
    @property
    @abstractmethod
    def is_undecided(self):
        """Returns True IFF the game is undecided, i.e. there is no winner or a tie yet."""
        return False

    @property
    @abstractmethod
    def is_tie(self):
        """Returns True IFF the game ended in a tie."""
        return False
    
    @property
    @abstractmethod
    def is_win(self):
        """Returns True IFF the game ended with a winner."""
        return False

class Undecided(WinState):
    @property
    def is_undecided(self):
        return True
    
    def __bool__(self):
        return False
    
class Decided(WinState):
    @property
    def is_decided(self):
        return True
        
    def __bool__(self):
        return True

class Tie(Decided):
    @property
    def is_tie(self):
        return True

class Win(Decided):
    """
    Attributes:
        winner: The winner of the game
    """

    def __init__(self, winner):
        self.winner = winner

    @property
    def is_win(self):
        return True

class AbstractState(metaclass=ABCMeta):
    """Represent the state of a game at any particular time."""

    @property
    @abstractmethod
    def outcome(self) -> WinState:
        """Return the outcome of the current state."""

    @property
    @abstractmethod
    def current_player(self) -> int:
        """Return the player whose turn it is."""

    @abstractmethod
    def possible_moves(self) -> Collection[Any]:
        """The possible moves that can be made by the current player in this state.
        
        Returns:
            A collection of all possible moves that can be made by the current
            player.
        """
        pass

    @abstractmethod
    def next_move(self, player, move) -> AbstractState:
        """
        Get the next game state when the given player makes the selected move.
        
        Args:
            player: The player that makes the move
            move: The move made

        Returns:
            The state of the game after the player makes the move.
        """

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass