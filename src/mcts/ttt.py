from typing import Any, Collection
from itertools import cycle
from copy import deepcopy

from .state import AbstractState, Outcome, Win, Tie, Undecided

class TicTacToeState(AbstractState):
    """Game states for Tic Tac Toe.
    
    Attributes:
        N: (class constant) The size of the Tic Tac Toe grid.
        rows: The rows of the Tic Tac Toe game.
    """
    N = 3

    def __init__(self, rows=None, players=["X", "O"]):
        """
        Args:
            rows:
                The rows of the grid. If none, a new game is constructed.
            players:
                The player symbols (X, and O) in the order of who will play
                next. The player at the front of the list moves next."""
        if rows is None:
            # Construct a new game
            self.rows = [[' ' for i in range(TicTacToeState.N)] for i in range(TicTacToeState.N)]
        else:
            self.rows = rows
        
        # Create a cycling iterator to always have a next player
        self.players = cycle(players)
        self._player = next(self.players)


    def make_move(self) -> AbstractState:
        # What the hell is this method?
        raise NotImplementedError

    @property
    def outcome(self) -> Outcome:
        # Check for a win in the rows
        for row in self.rows:
            if all([sq == row[0] for sq in row]) and row[0] != ' ':
                return Win(row[0])
        
        # Check for a win in the columns
        for i in range(TicTacToeState.N):
            if all([row[i] == self.rows[0][i] for row in self.rows]) and self.rows[0][i] != ' ':
                return Win(self.rows[0][i])
        
        # Check for a win in the diagonal
        if all([self.rows[i][i] == self.rows[0][0] for i in range(TicTacToeState.N)]) and self.rows[0][0] != ' ':
            return Win(self.rows[0][0])
        
        # Check for a win in the opposite diagonal
        if all([self.rows[i][TicTacToeState.N - i - 1] == self.rows[0][TicTacToeState.N-1] for i in range(TicTacToeState.N)]) and self.rows[0][TicTacToeState.N-1] != ' ':
            return Win(self.rows[0][TicTacToeState.N-1])
        
        # Check for a tie
        for row in self.rows:
            if not all([sq != ' ' for sq in row]):
                break
        else:
            return Tie()
        
        return Undecided()

    @property
    def current_player(self) -> int:
        return self._player

    def possible_moves(self) -> Collection[Any]:
        # Return no possible moves if the game is decided. Theoretically this
        # shouldn't be necessary.
        if self.outcome.is_decided:
            return list()

        # Any blank square is a move
        moves = list()
        for y, row in enumerate(self.rows):
            for x, square in enumerate(row):
                if square != ' ':
                    continue

                # List moves in alpha-numeric coordinates
                moves.append(f"{chr(64 + TicTacToeState.N - y)}{x}")

        return moves

    def next_move(self, player, move) -> AbstractState:
        if move not in self.possible_moves():
            raise ValueError(f"Invalid move: {move}")
        
        # Parse the move string into numerical coordinates
        y = 64 + TicTacToeState.N - ord(move[0])
        x = int(move[1])

        rows = deepcopy(self.rows)
        rows[y][x] = self.current_player
        return TicTacToeState(rows, players=self.players)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TicTacToeState):
            return False
        
        return self.rows == value.rows and self.current_player == value.current_player

    def __str__(self) -> str:
        s = ""
        row_s = "{}  {} | {} | {} \n"
        for y, row in enumerate(self.rows):
            # s += row_s.format(*([' '] * (TicTacToeState.n + 1)))
            s += row_s.format(chr(64+TicTacToeState.N - y), *row)
            # s += row_s.format(*([' '] * (TicTacToeState.n + 1)))

            if y < len(self.rows) - 1:
                s += "  ---+---+---\n"

        s += "  " + "".join([f" {i}  " for i in range(TicTacToeState.N)]) + "\n"
        s += f"{self.current_player}'s turn"
        return s
    
    def __repr__(self) -> str:
        return "\n".join(["".join(row) for row in self.rows]).replace(' ', '_')

        

