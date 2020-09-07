from pygraphblas import Matrix
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol


def test_matrix_multiplication():
    matrix_1 = Matrix.from_lists(
        [0, 1, 2],
        [1, 2, 0],
        [1, 2, 3]
    )

    matrix_2 = Matrix.from_lists(
        [0, 1, 2],
        [1, 2, 0],
        [4, 5, 6]
    )

    result = matrix_1 @ matrix_2

    expected = Matrix.from_lists(
        [0, 1, 2],
        [2, 0, 1],
        [5, 12, 12]
    )

    assert result.iseq(expected)


def test_automata_intersection():
    states = [State(str(i)) for i in range(6)]
    symb_a = Symbol('a')
    symb_b = Symbol('b')
    symb_c = Symbol('c')

    enfa_1 = EpsilonNFA()
    enfa_1.add_start_state(states[0])
    enfa_1.add_transitions([
        (states[0], symb_a, states[1]),
        (states[1], symb_b, states[2]),
        (states[2], symb_c, states[0])
    ])
    enfa_1.add_final_state(states[0])

    enfa_2 = EpsilonNFA()
    enfa_2.add_start_state(states[3])
    enfa_2.add_transitions([
        (states[3], symb_a, states[4]),
        (states[4], symb_b, states[4]),
        (states[4], symb_c, states[5])
    ])
    enfa_2.add_final_state(states[5])

    result = enfa_1 & enfa_2

    expected = EpsilonNFA()
    expected.add_start_state(states[0])
    expected.add_transitions([
        (states[0], symb_a, states[1]),
        (states[1], symb_b, states[2]),
        (states[2], symb_c, states[3])
    ])
    expected.add_final_state(states[3])

    assert result.is_equivalent_to(expected)
