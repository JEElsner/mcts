from typing import Dict

from .state import AbstractState, Tie
from .agents import Agent

class Game:
    """
    A simple turn-based game.

    Attributes:
        state:
            The current game state
        agents:
            The players playing the game. Maps the representation of the
            player (a name or symbol) to the agent.
    """

    def __init__(self, start_state: AbstractState, agents: Dict[str, Agent]):
        """Construct a game.
        
        Args:
            start_state:
                The starting state of the game.
            agents:
                The agents playing the game. Mapping of the representation of
                the player to the
            agent."""
        self.state = start_state
        self.agents = agents

    def play(self):
        """Play the game until it is decided.
        
        Agents take turns making moves, and game notifies the other agents of
        the moves made.
        
        Returns:
            The final game state, guaranteed to be decided.
        """

        # Play until there is an outcome
        while self.state.outcome.is_undecided:
            player = self.state.current_player
            move = self.agents[player].make_move(self.state)

            # Check to make sure the agent chose a valid move
            if move not in self.state.possible_moves():
                raise ValueError(f"{player} selected move invalid move {move}")
            
            # Move to the next state
            next_state = self.state.next_move(player, move)

            # Notify the other players that a move was made
            for observer, agent in self.agents.items():
                if observer == player:
                    continue

                agent.observe_move(player, move, next_state)

            self.state = next_state

        ### The game is now decided ###

        # Show the players the final game state
        for observer, agent in self.agents.items():
            agent.see_state(self.state)

        # Print the outcome
        if self.state.outcome.is_tie:
            print("The game ends in a tie.")
        else:
            print(f"The winner is {self.state.outcome.winner}")

        return self.state
                