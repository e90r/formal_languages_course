from pyformlang.finite_automaton import FiniteAutomaton, State, Symbol
from pyformlang.finite_automaton.nondeterministic_finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from pyformlang.regular_expression import python_regex
from pygraphblas import Matrix, BOOL
from pygraphblas import semiring


# Graph represented with Boolean Matrices
class BMGraph:
    def __init__(self, automaton: FiniteAutomaton = None):
        self.states_amount = 0
        self.states = set()
        self.start_states = set()
        self.final_states = set()
        self.values = set()
        self.matrices = dict()

        if (automaton is not None):
            self.states_amount = len(automaton.states)
            self.__states_dict = dict([(state, index) for (
                index, state) in enumerate(automaton.states)])
            self.states = set([self.__states_dict[state]
                               for state in automaton.states])
            self.start_states = set([self.__states_dict[state]
                                     for state in automaton.start_states])
            self.final_states = set([self.__states_dict[state]
                                     for state in automaton.final_states])
            self.values = set([symbol.value for symbol in automaton.symbols])
            self.matrices = self.__create_bool_matrices__(automaton)

    def __create_bool_matrices__(self, automaton: FiniteAutomaton):
        bool_matrices = {}
        transitions_dict = {}

        for (v_from, dict_to) in automaton.to_dict().items():
            new_dict_to = {}
            for (value, v_to) in dict_to.items():
                new_dict_to[value] = self.__states_dict[v_to]
            transitions_dict[self.__states_dict[v_from]] = new_dict_to

        for (v_from, dict_to) in transitions_dict.items():
            for (value, v_to) in dict_to.items():
                matrix = bool_matrices.get(value, Matrix.sparse(
                    BOOL, self.states_amount, self.states_amount))
                matrix[v_from, v_to] = True
                bool_matrices[value] = matrix

        return bool_matrices

    def dup(self):
        res = BMGraph()

        res.states_amount = self.states_amount
        res.states = self.states
        res.start_states = self.start_states
        res.final_states = self.final_states
        res.values = self.values

        for label, matrix in self.matrices.items():
            res.matrices[label] = matrix.dup()

        return res

    def to_automaton(self):
        nfa = NondeterministicFiniteAutomaton()

        for s in self.start_states:
            nfa.add_start_state(State(s))
        for s in self.final_states:
            nfa.add_final_state(State(s))
        for (value, matrix) in self.matrices.items():
            reachable = BMGraph.get_reachable_vertices(matrix)
            for (v_from, v_to) in reachable:
                nfa.add_transition(State(v_from), Symbol(value), State(v_to))

        return nfa

    def intersect(self, other):
        intersection = BMGraph()
        intersection.states_amount = self.states_amount * other.states_amount
        intersection.values = self.values

        for (value, self_bool_matrix) in self.matrices.items():
            if (value in other.matrices.keys()):
                other_bool_matrix = other.matrices[value]
                intersection.matrices[value] = self_bool_matrix.kronecker(
                    other_bool_matrix)

        for i in self.states:
            for j in other.states:
                intersection.states.add(i * other.states_amount + j)
                if (i in self.start_states and j in other.start_states):
                    intersection.start_states.add(i * other.states_amount + j)
                if (i in self.final_states and j in other.final_states):
                    intersection.final_states.add(i * other.states_amount + j)

        return intersection

    def transitive_closure(self):
        closure = Matrix.sparse(BOOL, self.states_amount, self.states_amount)

        with semiring.LOR_LAND_BOOL:
            for matrix in self.matrices.values():
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

    def get_reachable_vertices(matrix):
        reachable = list()

        matrix_lists = matrix.to_lists()
        for i in range(len(matrix_lists[0])):
            v_from = matrix_lists[0][i]
            v_to = matrix_lists[1][i]
            reachable.append((v_from, v_to))

        return reachable

    def from_edges_list(edges_list):
        graph = BMGraph()

        for (v_from, _, v_to) in edges_list:
            graph.states.add(v_from)
            graph.states.add(v_to)

        graph.states_amount = len(graph.states)
        graph.start_states = graph.states
        graph.final_states = graph.states

        for (v_from, value, v_to) in edges_list:
            graph.values.add(value)
            matrix = graph.matrices.get(value, Matrix.sparse(
                BOOL, graph.states_amount, graph.states_amount))
            matrix[v_from, v_to] = True
            graph.matrices[value] = matrix

        return graph

    def from_edges_file(path):
        edges_list = list()

        with open(path, 'r') as g:
            for line in g.readlines():
                edge = line.replace('\n', '').split(' ')
                v_from = int(edge[0])
                value = edge[1].strip()
                v_to = int(edge[2])
                edges_list.append((v_from, value, v_to))

        return BMGraph.from_edges_list(edges_list)

    def from_regex_string(regex, python_regex=True):
        if python_regex:
            dfa = Regex.from_python_regex(
                regex).to_epsilon_nfa().to_deterministic().minimize()
        else:
            dfa = Regex(regex).to_epsilon_nfa().to_deterministic().minimize()
        return BMGraph(dfa)

    def from_regex_file(path, python_regex=True):
        with open(path, 'r') as g:
            line = g.readline()
            return BMGraph.from_regex_string(line, python_regex)
