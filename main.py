from argparse import ArgumentParser
from benchmarks.cfpq_benchmark import cfpq_benchmark
from src.BMGraph import BMGraph


def read_vertices(path):
    with open(path, 'r') as f:
        return set([int(i) for i in f.readline().split(' ')])


def main():
    parser = ArgumentParser(description="""Intersect graph and regex,
                                        and show reachability of graph vertices""")
    parser.add_argument(
        'path_to_graph',
        help='Path to graph represented in \'from value to\' tuples'
    )
    parser.add_argument(
        'path_to_regex',
        help='Path to regex'
    )
    parser.add_argument(
        '--from',
        dest='vertices_from',
        help='Optional: source vertices from graph in \'v1 v2 v3 ...\' form'
    )
    parser.add_argument(
        '--to',
        dest='vertices_to',
        help='Optional: destination vertices from graph in \'v1 v2 v3 ...\' form'
    )
    args = parser.parse_args()

    graph = BMGraph.from_edges_file(args.path_to_graph)
    regex = BMGraph.from_regex_file(args.path_to_regex)

    if args.vertices_from is not None:
        vertices = read_vertices(args.vertices_from)
        graph.start_states = vertices

    if args.vertices_to is not None:
        vertices = read_vertices(args.vertices_to)
        graph.final_states = vertices

    intersection = graph.intersect(regex)

    print('Edges for each label:')

    for (value, matrix) in intersection.matrices.items():
        print('{} has {} edges'.format(value, matrix.nvals))

    closure = intersection.transitive_closure()

    print('Reachable vertices:')

    reachable = BMGraph.get_reachable_vertices(closure)
    for (v_from, v_to) in reachable:
        if v_from in intersection.start_states and v_to in intersection.final_states:
            print('{} -> {}'.format(v_from // regex.states_amount,
                                    v_to // regex.states_amount))


if __name__ == "__main__":
    cfpq_benchmark()
