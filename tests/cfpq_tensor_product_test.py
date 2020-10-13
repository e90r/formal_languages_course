import os
from src.BMGraph import BMGraph
from src.GrammarAlgos import GrammarAlgos


def test_cfpq_tensor_1():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test1')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.cfpq_tensor_product(grammar, graph)

    expected = {(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual


def test_cfpq_tensor_2():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test2')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.cfpq_tensor_product(grammar, graph)

    expected = {(0, 1), (3, 3)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual


def test_cfpq_tensor_3():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test3')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.cfpq_tensor_product(grammar, graph)

    expected = {(0, 0), (1, 1), (0, 2), (3, 3), (2, 2)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual


def test_cfpq_tensor_4():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test4')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.cfpq_tensor_product(grammar, graph)

    expected = {(0, 1), (4, 4), (2, 4), (1, 2),
                (0, 4), (3, 4), (0, 0), (4, 3), 
                (1, 1), (0, 3), (1, 4), (2, 3), 
                (0, 2), (3, 3), (2, 2), (1, 3)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual
