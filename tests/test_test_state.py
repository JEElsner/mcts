from . import TestState

import pytest

def test_init():
    s = TestState()
    assert s.current_player == 'A'

def test_possible_moves():
    s = TestState()
    assert s.possible_moves() == [1, 2, 3]

def test_next_state():
    s = TestState()
    assert s.next_move('A', 1) == TestState([('A', 1)], players=['B', 'A'])
    assert s == TestState()

def test_bad_moves():
    s = TestState()

    with pytest.raises(ValueError, match='player'):
        s.next_move('B', 1)

    with pytest.raises(ValueError, match='move'):
        s.next_move('A', 0)

def test_outcomes():
    s = TestState()
    assert s.outcome.is_undecided

    assert TestState(rounds=[('A', 1), ('B', 1), ('A', 1), ('B', 2)]).outcome.winner == 'A'
    assert TestState(rounds=[('A', 1), ('B', 2), ('A', 1), ('B', 2)]).outcome.is_tie

def test_false_eq():
    s1 = TestState()
    s2 = TestState(players=['B', 'A'])
    s3 = TestState(rounds=[('B', 1)])
    s4 = TestState(n_rounds=5)
    s5 = TestState(moves=[1,2,3,4])

    assert s1 != s2
    assert s1 != s3
    assert s1 != s4
    assert s1 != s5
    assert s1 != 'foo'

def test_str():
    assert str(TestState()) == "[] Turn: A"
