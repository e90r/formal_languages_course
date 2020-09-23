import os
import time
from pygraphblas import semiring

from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL

from src.BMGraph import BMGraph


def transitive_closure_sq(graph):

    closure = Matrix.sparse(BOOL, graph.states_amount, graph.states_amount)

    with semiring.LOR_LAND_BOOL:
        for matrix in graph.matrices.values():
            closure += matrix

    old_nvals = -1
    new_nvals = closure.nvals
    while old_nvals != new_nvals:
        with semiring.LOR_LAND_BOOL:
            closure += closure @ closure
        old_nvals = new_nvals
        new_nvals = closure.nvals

    return closure


def transitive_closure_mp(graph):
    closure = Matrix.sparse(BOOL, graph.states_amount, graph.states_amount)

    with semiring.LOR_LAND_BOOL:
        for matrix in graph.matrices.values():
            closure += matrix

    temp = closure.dup()
    old_nvals = -1
    new_nvals = closure.nvals
    while old_nvals != new_nvals:
        with semiring.LOR_LAND_BOOL:
            closure += temp @ closure
        old_nvals = new_nvals
        new_nvals = closure.nvals

    return closure


def closure_benchmark():
    path_to_data = os.path.join(os.getcwd(), 'benchmarks/refinedDataForRPQ')
    tests = ['LUBM1.9M']

    for test in tests:
        path_to_test = os.path.join(path_to_data, test)
        graph = BMGraph.from_edges_file('{}/{}.txt'.format(path_to_test, test))

        output = open('{}/output.csv'.format(path_to_test), 'w+')

        regex_dir = os.path.join(path_to_test, 'regexes')
        for filename in os.listdir(regex_dir):
            closure = None
            res = None
            regex_str = os.path.join(regex_dir, filename)
            regex = BMGraph.from_regex_file(regex_str, False)

            sum = 0
            for _ in range(5):
                start = time.monotonic()
                res = graph.intersect(regex)
                closure = transitive_closure_sq(res)
                end = time.monotonic()

                sum += end - start

            sq_pairs = closure.nvals
            sq_time = sum / 5

            start = time.monotonic()
            for (value, matrix) in res.matrices.items():
                v, n = value, matrix.nvals
            end = time.monotonic()

            sq_pairs_time = end - start

            sum = 0
            for _ in range(5):
                start = time.monotonic()
                res = graph.intersect(regex)
                closure = transitive_closure_mp(res)
                end = time.monotonic()

                sum += end - start

            mp_pairs = closure.nvals
            mp_time = sum / 5

            start = time.monotonic()
            for (value, matrix) in res.matrices.items():
                v, n = value, matrix.nvals
            end = time.monotonic()

            mp_pairs_time = end - start

            if (sq_pairs != mp_pairs):
                print('{}, {}, {}'.format(sq_pairs, mp_pairs, filename))

            assert sq_pairs == mp_pairs

            output.write('{:s},{:s},{:d},{:.3f},{:.3f},{:d},{:.3f},{:.3f}\r\n'.format(
                test, filename, sq_pairs, sq_time, sq_pairs_time, mp_pairs, mp_time, mp_pairs_time))

        output.close()
