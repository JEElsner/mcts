from abc import ABCMeta, abstractmethod
from typing import Any

from .state import AbstractState

class Agent(metaclass=ABCMeta):
    @abstractmethod
    def make_move(self, state: AbstractState) -> Any:
        pass

    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        pass

    def see_state(self, state: AbstractState) -> None:
        pass


class ConsoleAgent(Agent):
    def make_move(self, state: AbstractState) -> Any:
        print(state)
        
        while True:
            move = input("> ")
            if move in state.possible_moves():
                break
            else:
                print("Not a valid move!")

        return move
    
    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        print(f"{player} made move {move}.")

    def see_state(self, state: AbstractState) -> None:
        print(state)