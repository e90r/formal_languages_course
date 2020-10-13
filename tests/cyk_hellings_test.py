import os
from src.BMGraph import BMGraph
from src.GrammarAlgos import GrammarAlgos


# parentheses
def test_cyk_1():
    test_path = os.path.join(os.getcwd(), 'tests/data/cyk/test1')

    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    assert GrammarAlgos.CYK(grammar, 'aabbab')
    assert GrammarAlgos.CYK(grammar, 'ab')
    assert GrammarAlgos.CYK(grammar, 'ababab')
    assert GrammarAlgos.CYK(grammar, '')
    assert not GrammarAlgos.CYK(grammar, 'aa')
    assert not GrammarAlgos.CYK(grammar, 'aabbb')


# even length palindrome
def test_cyk_2():
    test_path = os.path.join(os.getcwd(), 'tests/data/cyk/test2')

    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    assert GrammarAlgos.CYK(grammar, 'aabbaa')
    assert GrammarAlgos.CYK(grammar, 'aaaa')
    assert GrammarAlgos.CYK(grammar, '')
    assert not GrammarAlgos.CYK(grammar, 'aba')
    assert not GrammarAlgos.CYK(grammar, 'a')


# even number of 'b'
def test_cyk_3():
    test_path = os.path.join(os.getcwd(), 'tests/data/cyk/test3')

    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    assert GrammarAlgos.CYK(grammar, 'aabab')
    assert GrammarAlgos.CYK(grammar, 'bbbb')
    assert GrammarAlgos.CYK(grammar, 'aaabb')
    assert not GrammarAlgos.CYK(grammar, 'ab')
    assert not GrammarAlgos.CYK(grammar, 'aabbab')


# classic example
def test_hellings_1():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test1')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.Hellings(grammar, graph)

    expected = {(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual


# random test from my head
def test_hellings_2():
    test_path = os.path.join(os.getcwd(), 'tests/data/cfpq/test2')

    graph = BMGraph.from_edges_file(
        os.path.join(test_path, 'graph.txt'))
    grammar = GrammarAlgos.from_grammar_file(
        os.path.join(test_path, 'grammar.txt'))

    adj_matrix = GrammarAlgos.Hellings(grammar, graph)

    expected = {(0, 1), (3, 3)}
    actual = set(BMGraph.get_reachable_vertices(adj_matrix))

    assert expected == actual
