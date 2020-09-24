import os
import random

import pytest

from pyformlang.finite_automaton.nondeterministic_finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton.symbol import Symbol

from src.BMGraph import BMGraph


def test_intersection_1():
    test_path = os.path.join(os.getcwd(), 'tests/data/test1')

    graph = BMGraph.from_edges_file(os.path.join(test_path, 'graph.txt'))
    regex = BMGraph.from_regex_file(os.path.join(test_path, 'regex.txt'))
    intersection = graph.intersect(regex)

    ans = intersection.to_automaton()
    a = Symbol('a')
    b = Symbol('b')

    assert ans.accepts([])
    assert ans.accepts([a])
    assert ans.accepts([a, a, a])
    assert not ans.accepts([b])


def test_intersection_2():
    test_path = os.path.join(os.getcwd(), 'tests/data/test2')

    graph = BMGraph.from_edges_file(os.path.join(test_path, 'graph.txt'))
    regex = BMGraph.from_regex_file(os.path.join(test_path, 'regex.txt'))
    intersection = graph.intersect(regex)

    ans = intersection.to_automaton()
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')

    assert ans.accepts([a, b, c])
    assert ans.accepts([a, c])
    assert ans.accepts([a, c, c])
    assert ans.accepts([a, b, c, c])
    assert not ans.accepts([a])
    assert not ans.accepts([b])
    assert not ans.accepts([b, c])
    assert not ans.accepts([a, b, b])
    assert not ans.accepts([a, b, b, c])


def test_intersection_3():
    test_path = os.path.join(os.getcwd(), 'tests/data/test3')

    graph = BMGraph.from_edges_file(os.path.join(test_path, 'graph.txt'))
    regex = BMGraph.from_regex_file(os.path.join(test_path, 'regex.txt'))
    intersection = graph.intersect(regex)

    ans = intersection.to_automaton()
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')

    assert not ans.accepts([a])
    assert not ans.accepts([b])
    assert not ans.accepts([c])
    assert not ans.accepts([a, b])
    assert not ans.accepts([a, b, c])


def test_intersection_4():
    test_path = os.path.join(os.getcwd(), 'tests/data/test4')

    graph = BMGraph.from_edges_file(os.path.join(test_path, 'graph.txt'))
    regex = BMGraph.from_regex_file(os.path.join(test_path, 'regex.txt'))
    intersection = graph.intersect(regex)

    ans = intersection.to_automaton()
    a = Symbol('a')
    b = Symbol('b')

    assert ans.accepts([a])
    assert ans.accepts([b])
    assert ans.accepts([a, b])
    assert not ans.accepts([a, a, b])
    assert not ans.accepts([a, b, b])


@pytest.fixture(scope="function", params=[
    (vertices_num, regex)
    for regex in ['a*b*c*', '(a|b)+(c|d)*', 'a?b*c+d']
    for vertices_num in [10, 50, 100, 500]
])
def random_data(request):
    vertices_num, regex_str = request.param
    edges_num = vertices_num * (vertices_num - 1) // 5
    v_from = [random.randint(0, vertices_num) for _ in range(edges_num)]
    v_to = [random.randint(0, vertices_num) for _ in range(edges_num)]
    values = [random.choice(['a', 'b', 'c', 'd']) for _ in range(edges_num)]
    edges_list = zip(v_from, values, v_to)
    graph = BMGraph.from_edges_list(edges_list)
    regex = BMGraph.from_regex_string(regex_str)
    return graph, regex


def test_intersection_random(random_data):
    graph, regex = random_data
    intersection = graph.intersect(regex)

    for (value, matrix) in intersection.matrices.items():
        matrix_lists = matrix.to_lists()
        for i in range(len(matrix_lists[0])):
            v_from = matrix_lists[0][i]
            v_to = matrix_lists[1][i]

            graph_from, graph_to = v_from // regex.states_amount, v_to // regex.states_amount
            regex_from, regex_to = v_from % regex.states_amount, v_to % regex.states_amount

            assert matrix[v_from, v_to] == 1
            assert graph.matrices[value][graph_from, graph_to] == 1
            assert regex.matrices[value][regex_from, regex_to] == 1
