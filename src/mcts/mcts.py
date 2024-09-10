from __future__ import annotations

from typing import Any, Dict, Hashable

from collections import Counter

import math
from random import Random

import warnings

from .state import AbstractState, Win, Tie, Undecided, Decided
from .agents import Agent

def default_score_function(node_wins, node_simulations, parent_simulations, exploration_parameter=math.sqrt(2)):
    return node_wins / node_simulations + exploration_parameter * math.sqrt(math.log(parent_simulations) / node_simulations)


class MCTSAgent(Agent):
    def __init__(self):
        self.root:Node = None
        self.curr_node: Node = None

    def make_move(self, state: AbstractState):
        if self.curr_node.state != state:
            warnings.warn("Current state of game does not match current state of MCT! Continuing with game state, but children may differ.")
            self.curr_node.state = state

        expansion_node = self.curr_node.select()
        expansion_node.expand()
        return self.curr_node.best_move

    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        if self.curr_node is None:
            self.root = Node(new_state)
            self.curr_node = self.root
            return
        else:
            next_node = self.curr_node.children.get(move, None)

        if next_node is None:
            next_node = Node(new_state, Counter(), parent=self.curr_node)
        elif next_node.state != new_state:
            next_node.state = new_state
            warnings.warn("Next state does not match expected next state in MCT. Continuing with game-provided next state, but children may differ.")
        
        self.curr_node = next_node
        

class Node:
    def __init__(self, state: AbstractState, scores=Counter(), children: Dict[Hashable, Node] = dict(), rng=None, score_fn=default_score_function, parent=None):
        """Create a node in the Monte Carlo search tree"""
        if rng is None:
            self.rng = Random()
        else:
            self.rng = rng

        self.state = state
        self.children = children
        self.scores = scores
        self.score_fn = score_fn
        self.parent = parent

    def select(self):
        """Select a node to expand in exploration"""
        if len(self.children) == 0:
            return self
        else:
            parent_simulations = self.scores.total()
            next_state = max(self.children.values(), key=lambda s: s.score(parent_simulations))
            return next_state.select()

    def score(self, parent_simulations, player=None, **kwargs):
        """Score the current node for its exploratory/exploitatory potential"""
        if player is None:
            player = self.state.current_player

        node_wins = self.scores[player]
        node_simulations = self.scores.total()
        return self.score_fn(node_wins, node_simulations, parent_simulations)

    def expand(self):
        """Try different moves at this state, checking which ones are effective."""
        # TODO limit to less than all possible moves
        if not isinstance(self.state.winner, Undecided):
            return

        for move in self.state.possible_moves():
            self.children[move] = Node(self.state.next_move(self.state.current_player, move), parent=self)
            self.children[move].simulate()

    def simulate(self):
        """Simulate a playout of the current node"""
        if isinstance(self.state.winner, Win):
            self.scores[self.state.winner.winner] += 1
            self.backpropagate()
        elif isinstance(self.state.winner, Tie):
            pass
            # TODO: partial points for tie?
        else:
            move = self.rng.choice(self.state.possible_moves())
            self.children[move] = Node(self.state.next_move(self.state.current_player, move), parent=self)
            self.children[move].simulate()

        return self.scores
    
    def backpropagate(self):
        if self.parent is not None:
            self.parent.scores += self.scores
            self.parent.backpropagate()
    
    @property
    def best_move(self, player=None):
        """The current best move that can be made by the player."""
        if player is None:
            player = self.state.current_player

        return max(self.children.keys(), key=lambda k: self.children[k].scores[player])

