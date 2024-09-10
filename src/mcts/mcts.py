from __future__ import annotations

from typing import Any, Dict, Hashable

from collections import Counter

import math
from random import Random

import warnings

from .state import AbstractState, Win, Tie, Undecided, Decided
from .agents import Agent

class MockRng:
    def randint(self, a, b):
        return 0
    
    def choice(self, collection):
        return collection[0]

def default_score_function(node_wins, node_simulations, parent_simulations, exploration_parameter=math.sqrt(2)) -> float:
    """Score the value of the node for a player.
    
    Args:
        node_wins:
            The number of wins for the player at this node
        node_simulations:
            The number of times this node has been simulated to a conclusion.
        parent_simulations:
            The number of times the parent of this node has been simulated.
        exploration_parameter:
            Constant balancing exploration vs exploitation. Higher values
            prioritize exploration.
        
    Returns:
        The relative value of the node. A higher value means the node will be
        explored and exploited more often.
    """
    return node_wins / node_simulations + exploration_parameter * math.sqrt(math.log(parent_simulations) / node_simulations)


class MCTSAgent(Agent):
    """A player agent that makes decisions using Monte Carlo Tree Search.
    
    Attributes:
        root: The root node of the game played.
        curr_node: The node containing the current state of the game played.
    """

    def __init__(self):
        """Initialize the MCTS agent."""

        self.root:Node = None
        self.curr_node: Node = None

    def make_move(self, state: AbstractState):
        """Explore possible moves and pick the best one.

        Args:
            state: The current state of the game.
        
        Returns:
            The chosen move to make from the possible moves at this game state.
        """

        if self.curr_node.state != state:
            warnings.warn("Current state of game does not match current state of MCT! Continuing with game state, but children may differ.")
            self.curr_node.state = state

        # Select, expand, and choose the best move
        return self.curr_node.playout()

    def observe_move(self, player: Any, move: Any, new_state: AbstractState) -> None:
        """Observe a move made by another player, updating the state tree.
        
        Args:
            player: The player making the move.
            move: The move made.
            new_state: The new state of the game.
        """
        # If the game has just started, set the root
        if self.curr_node is None:
            self.root = Node(new_state, rng=MockRng())
            self.curr_node = self.root
            return
        else:
            # Otherwise, try to move down the pre-existing tree
            next_node = self.curr_node.children.get(move, None)

        if next_node is None:
            # This is a novel game state unseen before
            next_node = Node(new_state, Counter(), parent=self.curr_node, rng=self.root.rng)
        elif next_node.state != new_state:
            # We've seen this move before, but it led to a state not in the
            # tree. Theoretically, this shouldn't happen.
            next_node.state = new_state
            warnings.warn("Next state does not match expected next state in MCT. Continuing with game-provided next state, but children may differ.")
        
        self.curr_node = next_node

    def see_state(self, state: AbstractState) -> None:
        # TODO complete
        pass

        

class Node:
    def __init__(self, state: AbstractState, scores=None, children: Dict[Hashable, Node] = dict(), rng=None, score_fn=default_score_function, parent=None):
        """Create a node for a Monte Carlo search tree.
        Args:
            state:
                The game state to store in the node
            scores:
                The win counts of the players at this node.
            children:
                A mapping of the possible moves in this game state to the game states reached by making those moves.
            rng:
                The random object to use for exploration
            score_fn:
                The function to score the node for exploitability/explorability.
            parent:
                The parent node of this one.
        """
        if scores is None:
            scores = Counter()

        # Initialize rng if none is provided.
        if rng is None:
            self.rng = Random()
        else:
            self.rng = rng

        self.state = state
        self.children = children
        self.scores = scores
        self.score_fn = score_fn
        self.parent = parent
        
    def playout(self, n_moves=10):
        """Temporary function until full functionality is achieved."""

        # Select node to explore
        chain = [self]
        while len(chain[-1].children) != 0:
            if len(chain) > 1:
                parent_simulations = max(chain[-2].scores.total(), 1)
            else:
                parent_simulations = 1
            
            chain.append(
                max(chain[-1].children.values(), key=lambda s: s.score(parent_simulations))
            )

        # Expand multiple moves from exploration node
        expansion_moves = chain[-1].state.possible_moves()
        for i in range(min(n_moves, len(expansion_moves))):
            expansion_chain = [chain[-1]]
            move = expansion_moves.pop(self.rng.randint(0, len(expansion_moves)-1))

            # Simulate playout with given move
            while expansion_chain[-1].state.outcome.is_undecided:
                if move is None:
                    move = self.rng.choice(expansion_chain[-1].state.possible_moves())

                node = Node(expansion_chain[-1].state.next_move(
                        expansion_chain[-1].state.current_player,
                        move,
                    ),
                    rng=expansion_chain[-1].rng)
                expansion_chain[-1].children[move] = node
                expansion_chain.append(node)
                
                move = None
                
            
            # Check the outcome
            if expansion_chain[-1].state.outcome.is_tie:
                # outcome is a tie
                # TODO: partial points for ties?
                # Need to increment something by one to account for simulation counts
                expansion_chain[-1].scores[None] += 1
            else:
                # outcome is a win
                winner = expansion_chain[-1].state.outcome.winner
                expansion_chain[-1].scores[winner] +=1
            
            # Backpropagate wins back to expansion node
            for i, node in enumerate(expansion_chain[-2::-1]):
                node.scores += expansion_chain[i+1].scores
                
        # Backpropagate wins from expanded node to self node
        for i, node in enumerate(chain[-2::-1]):
            node.scores += expansion_chain[i+1].scores
            
        # Return best move in current state
        return max(self.children.keys(), key=lambda k: self.children[k].scores[self.state.current_player])


    def select(self):
        """Select a node to expand in exploration.
        
        Returns:
            The selected leaf node in the MCT to explore.
        """
        if len(self.children) == 0:
            # Select this node for exploration, since it has no children
            return self
        else:
            # Recursively select child nodes until we reach a leaf using the
            # explore/exploit potential of the nodes.
            parent_simulations = self.scores.total()
            next_state = max(self.children.values(), key=lambda s: s.score(parent_simulations))
            return next_state.select()

    def score(self, parent_simulations, player=None, **kwargs):
        """Score the current node for its exploratory/exploitatory potential.
        
        Args:
            parent_simulations:
                The number of times the parent node has been simulated.
            player:
                The player for which the node is scored
        
        Returns:
            The score of the node. Higher means the node has more potential to
            the player.
        """
        # Select current player if none passed.
        if player is None:
            player = self.state.current_player

        node_wins = self.scores[player]
        node_simulations = self.scores.total()
        if node_simulations == 0:
            # Avoid divide by zero errors
            node_simulations = 1
        return self.score_fn(node_wins, node_simulations, parent_simulations)

    def expand(self):
        """Try different moves at this state, checking which ones are effective."""
        # TODO limit to less than all possible moves

        # If the game is decided now, we cannot expand
        if self.state.outcome.is_decided:
            return

        # Try all the possible moves in this state (see TODO above)
        for move in self.state.possible_moves():
            self.children[move] = Node(self.state.next_move(self.state.current_player, move), parent=self)
            self.children[move].simulate()

    def simulate(self):
        """Simulate a playout of the current node
        
        Returns:
            The updated win counts of for the players at this node.
        """
        if self.state.outcome.is_win:
            # Update win counts if someone has won
            self.scores[self.state.outcome.winner] += 1
            self.backpropagate()
        elif self.state.outcome.is_tie:
            pass
            # TODO: partial points for tie?
        else:
            # Make moves until this playout is decided
            move = self.rng.choice(self.state.possible_moves())
            self.children[move] = Node(self.state.next_move(self.state.current_player, move), parent=self)
            self.children[move].simulate()

        return self.scores
    
    def backpropagate(self):
        """Update the win scores for the parents of this node."""
        if self.parent is not None:
            self.parent.scores += self.scores
            self.parent.backpropagate()
    
    @property
    def best_move(self, player=None):
        """The current best move that can be made by the player.
        
        Returns:
            The best move to make for the player at the current game state.
        """
        # Select current player if none provided
        if player is None:
            player = self.state.current_player

        # Choose the best move based on win counts
        return max(self.children.keys(), key=lambda k: self.children[k].scores[player])

