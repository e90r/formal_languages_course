from argparse import ArgumentParser
from BMGraph import BMGraph


def read_vertices(path):
    with open(path, 'r') as f:
        return set([int(i) for i in f.readline().split(' ')])


def main():
    parser = ArgumentParser(description="""Intersect graph and regex,
                                        and show reachability of graph vertices""")
    parser.add_argument(
        'path_to_graph',
        help='Path to graph represented in (from, value, to) tuples'
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

    graph = BMGraph.from_edges(args.path_to_graph)
    regex = BMGraph.from_regex(args.path_to_regex)

    if args.vertices_from is not None:
        vertices = read_vertices(args.vertices_from)
        graph.start_states = vertices

    if args.vertices_to is not None:
        vertices = read_vertices(args.vertices_to)
        graph.final_states = vertices

    intersection = graph.intersect(regex)

    closure = intersection.transitive_closure()

    reachable = BMGraph.get_reachable_vertices(closure)
    for (v_from, v_to) in reachable:
        v_from = intersection.states_dict[v_from]
        v_to = intersection.states_dict[v_to]
        if v_from in intersection.start_states and v_to in intersection.final_states:
            print('{} -> {}'.format(v_from // graph.states_amount, v_to // graph.states_amount))


if __name__ == "__main__":
    main()
