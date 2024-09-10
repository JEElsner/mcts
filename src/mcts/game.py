from typing import Dict

from .state import AbstractState, Tie
from .agents import Agent

class Game:
    def __init__(self, start_state: AbstractState, agents: Dict[str, Agent]):
        self.state = start_state
        self.agents = agents

    def play(self):
        while not self.state.winner:
            player = self.state.current_player
            move = self.agents[player].make_move(self.state)

            if move not in self.state.possible_moves():
                raise ValueError(f"{player} selected move invalid move {move}")
            
            next_state = self.state.next_move(player, move)
            for observer, agent in self.agents.items():
                if observer == player:
                    continue

                agent.observe_move(player, move, next_state)

            self.state = next_state

        for observer, agent in self.agents.items():
            agent.see_state(self.state)

        if isinstance(self.state.winner, Tie):
            print("The game ends in a tie.")
        else:
            print(f"The winner is {self.state.winner.winner}")
                