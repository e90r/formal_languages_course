import os
import time

from src.GrammarAlgos import GrammarAlgos
from src.BMGraph import BMGraph


def cfpq_benchmark():
    path_to_data = os.path.join(os.getcwd(), 'benchmarks/dataForCFPQ')
    tests = ['FullGraph', 'MemoryAliases', 'WorstCase']

    for test in tests:
        path_to_test = os.path.join(path_to_data, test)

        output = open('{}/output.csv'.format(path_to_test), 'w+')
        output.write('test,graph,grammar,algo_name,algo_time\r\n')

        graph_dir = os.path.join(path_to_test, 'graphs')
        # for graph_name in sorted(os.listdir(graph_dir), key=lambda s: int(s.split('_')[1])):
        for graph_name in os.listdir(graph_dir):
            graph_path = os.path.join(graph_dir, graph_name)
            graph = BMGraph.from_edges_file(graph_path)

            grammar_dir = os.path.join(path_to_test, 'grammars')
            for grammar_name in os.listdir(grammar_dir):
                grammar_path = os.path.join(grammar_dir, grammar_name)
                grammar = GrammarAlgos.from_grammar_file(grammar_path)

                start = time.monotonic()
                hellings_res = GrammarAlgos.Hellings(grammar, graph)
                end = time.monotonic()

                algo_name = 'hellings'
                algo_time = end - start

                res_str = '{:s},{:s},{:s},{:s},{:.3f}\r\n'.format(
                    test, graph_name, grammar_name, algo_name, algo_time)
                print(res_str)
                output.write(res_str)

                start = time.monotonic()
                mult_res = GrammarAlgos.cfpq_matrix_multiplication(
                    grammar, graph)
                end = time.monotonic()

                algo_name = 'mult'
                algo_time = end - start

                res_str = '{:s},{:s},{:s},{:s},{:.3f}\r\n'.format(
                    test, graph_name, grammar_name, algo_name, algo_time)
                print(res_str)
                output.write(res_str)

                start = time.monotonic()
                tensor_res = GrammarAlgos.cfpq_tensor_product(grammar, graph)
                end = time.monotonic()

                algo_name = 'tensor'
                algo_time = end - start

                res_str = '{:s},{:s},{:s},{:s},{:.3f}\r\n'.format(
                    test, graph_name, grammar_name, algo_name, algo_time)
                print(res_str)
                output.write(res_str)

                wcnf = GrammarAlgos.to_wcnf(grammar)
                start = time.monotonic()
                tensor_wcnf_res = GrammarAlgos.cfpq_tensor_product(wcnf, graph)
                end = time.monotonic()

                algo_name = 'tensor_wcnf'
                algo_time = end - start

                res_str = '{:s},{:s},{:s},{:s},{:.3f}\r\n'.format(
                    test, graph_name, grammar_name, algo_name, algo_time)
                print(res_str)
                output.write(res_str)

                assert(hellings_res == mult_res)
                assert(mult_res == tensor_res)
                assert(tensor_res == tensor_wcnf_res)

        output.close()
