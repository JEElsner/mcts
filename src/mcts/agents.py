from abc import ABCMeta, abstractmethod
from typing import Any

from .state import AbstractState

class Agent(metaclass=ABCMeta):
    """A player agent."""

    @abstractmethod
    def make_move(self, state: AbstractState) -> Any:
        """
        Get a move to make from the agent.
        
        Args:
            state: The current state of the game.

        Returns:
            The move the agent wishes to make in the current state. The returned
            move should be one of `state.possible_moves()`.
        """

    @abstractmethod
    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        """
        Observe a move made by a different player agent.

        Args:
            player: The player that makes the move
            move: The move made
            new_state: The state of the game after the move is made
        """

    @abstractmethod
    def see_state(self, state: AbstractState) -> None:
        """
        Observe the state of the game.

        Args:
            state: The current state of the game
        """


class ConsoleAgent(Agent):
    """
    Prints out game states to the console and prompts for moves.

    Allows a human to play the game in the console.
    """

    def make_move(self, state: AbstractState) -> Any:
        """
        Prompt the user to make a move.

        Prints the current state of the game to the console and prompts the user
        for a move. If the user selects an invalid move, the user is prompted
        repeatedly until they select a valid move.

        Args:
            state: The current state of the game.

        Returns:
            The move selected by the
        """

        print(state)
        
        # Prompt for a move until the user provides a valid one
        while True:
            move = input("> ")
            if move in state.possible_moves():
                break
            else:
                print("Not a valid move!")

        return move
    
    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        """
        Notify the user that a move was made.

        Args:
            player: The player that made the move
            move: The move made
            new_state: The new state of the game
        """

        print(f"{player} made move {move}.")

    def see_state(self, state: AbstractState) -> None:
        """
        Show the user the current state of the game.

        Args:
            state: The current game state.
        """
        print(state)