from mcts.ttt import TicTacToeState
import pytest

def test_possible_moves():
    t = TicTacToeState()
    assert set(t.possible_moves()) == set(['C0', 'C1', 'C2', 'B0', 'B1', 'B2', 'A0', 'A1', 'A2'])
    
    t = TicTacToeState([['X', 'X', 'O'], ['O', 'O', ' '], ['X', 'O', 'X']])
    assert set(t.possible_moves()) == set(['B2'])
    
    t = TicTacToeState([['X' for i in range(3)] for i in range(3)])
    assert set(t.possible_moves()) == set()

def test_next_state():
    t1 = TicTacToeState()
    t2 = TicTacToeState([[' ', ' ', ' '], [' ', 'X', ' '], [' ', ' ', ' ']], players=['O', 'X'])

    assert t1.next_move('X', 'B1') == t2
    assert t1 == TicTacToeState()

    with pytest.raises(ValueError):
        t1.next_move('X', 'foo')

def test_win():
    t = TicTacToeState([[' ' for x in range(3)] for y in range(2)] + [['X', 'X', 'X']])
    assert t.outcome.is_win
    assert t.outcome.winner == 'X'

    t = TicTacToeState([['O', ' ', ' '] for y in range(3)])
    assert t.outcome.is_win
    assert t.outcome.winner == 'O'
    
    rows = [[' ' for i in range(3)] for j in range(3)]
    for i in range(3):
        rows[i][i] = 'X'
    t = TicTacToeState(rows)
    assert t.outcome.is_win
    assert t.outcome.winner == 'X'
    
    rows = [[' ' for i in range(3)] for j in range(3)]
    for i in range(3):
        rows[i][2-i] = 'X'
    t = TicTacToeState(rows)
    assert t.outcome.is_win
    assert t.outcome.winner == 'X'

    assert TicTacToeState().outcome.is_undecided

    t = TicTacToeState([
        ['X', 'X', 'O'],
        ['O', 'O', 'X'],
        ['X', 'O', 'O']
    ])
    assert t.outcome.is_tie

def test_eq():
    t1 = TicTacToeState()
    t2 = TicTacToeState()
    player_swap = TicTacToeState(players=["O", "X"])

    assert t1 == t2
    assert t1 != player_swap
    assert t1 != "foo"

def test_str():
    # TODO flesh out
    # although this one alone was stupid
    assert str(TicTacToeState()) == "C    |   |   \n  ---+---+---\nB    |   |   \n  ---+---+---\nA    |   |   \n   0   1   2  \nX's turn"

def test_repr():
    # TODO flesh out
    assert repr(TicTacToeState()) == '___\n___\n___'
