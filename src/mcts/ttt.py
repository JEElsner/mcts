from typing import Any, Collection
from itertools import cycle
from copy import deepcopy

from .state import AbstractState, Win, Tie, Undecided

class TicTacToeState(AbstractState):
    n = 3

    def __init__(self, rows=None, players=["X", "O"]):
        if rows is None:
            self.rows = [[' ' for i in range(TicTacToeState.n)] for i in range(TicTacToeState.n)]
        else:
            self.rows = rows
        
        self.players = cycle(players)
        self._player = next(self.players)


    def make_move(self) -> AbstractState:
        raise NotImplementedError

    @property
    def winner(self) -> Any:
        for row in self.rows:
            if all([sq == row[0] for sq in row]) and row[0] != ' ':
                return Win(row[0])
            
        for i in range(TicTacToeState.n):
            if all([row[i] == self.rows[0][i] for row in self.rows]) and self.rows[0][i] != ' ':
                return Win(self.rows[0][i])
            
        if all([self.rows[i][i] == self.rows[0][0] for i in range(TicTacToeState.n)]) and self.rows[0][0] != ' ':
            return Win(self.rows[0][0])
        
        if all([self.rows[i][TicTacToeState.n - i - 1] == self.rows[0][TicTacToeState.n-1] for i in range(TicTacToeState.n)]) and self.rows[0][TicTacToeState.n-1] != ' ':
            return Win(self.rows[0][TicTacToeState.n-1])
        
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
        if not isinstance(self.winner, Undecided):
            return list()

        moves = list()
        for y, row in enumerate(self.rows):
            for x, square in enumerate(row):
                if square != ' ':
                    continue

                moves.append(f"{chr(64 + TicTacToeState.n -y)}{x}")

        return moves

    def next_move(self, player, move) -> AbstractState:
        if move not in self.possible_moves():
            raise ValueError(f"Invalid move: {move}")
        
        y = 64 + TicTacToeState.n - ord(move[0])
        x = int(move[1])

        rows = deepcopy(self.rows)
        rows[y][x] = self.current_player
        return TicTacToeState(rows, players=self.players)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TicTacToeState):
            return False
        
        return self.rows == value.rows

    def __str__(self) -> str:
        s = ""
        row_s = "{}  {} | {} | {} \n"
        for y, row in enumerate(self.rows):
            # s += row_s.format(*([' '] * (TicTacToeState.n + 1)))
            s += row_s.format(chr(64+TicTacToeState.n - y), *row)
            # s += row_s.format(*([' '] * (TicTacToeState.n + 1)))

            if y < len(self.rows) - 1:
                s += "  ---+---+---\n"

        s += "  " + "".join([f" {i}  " for i in range(TicTacToeState.n)]) + "\n"
        s += f"{self.current_player}'s turn"
        return s
    
    def __repr__(self) -> str:
        return "\n".join(["".join(row) for row in self.rows]).replace(' ', '_')

        

