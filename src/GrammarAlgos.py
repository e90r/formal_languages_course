from collections import deque
from pyformlang.cfg import terminal
from pyformlang.cfg import production
from pyformlang.cfg.epsilon import Epsilon
from pyformlang.regular_expression import python_regex
from pyformlang.regular_expression.regex import Regex
from pygraphblas import semiring

from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL
from src.BMGraph import BMGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG

state_counter = 0


class GrammarAlgos:
    def to_wcnf(grammar):
        wcnf = grammar.to_normal_form()
        if grammar.generate_epsilon:
            new_start_symbol = Variable('S\'')
            new_variables = set(wcnf.variables)
            new_variables.add(new_start_symbol)
            new_productions = set(wcnf.productions)
            new_productions.add(Production(
                new_start_symbol, [wcnf.start_symbol]))
            new_productions.add(Production(new_start_symbol, []))
            return CFG(new_variables, wcnf.terminals, new_start_symbol, new_productions)
        return wcnf

    def prod_from_regex(head, regex, python_regex=False, nonterms_upper=True):
        if python_regex:
            regex = Regex.from_python_regex(regex)
        else:
            regex = Regex(regex)

        enfa = regex.to_epsilon_nfa().minimize()
        transitions = enfa.to_dict()
        state_to_var = dict()
        production_set = set()

        for state in enfa.states:
            global state_counter
            state_counter += 1
            state_to_var[state] = Variable(f'State{state_counter}')

        for start_state in enfa.start_states:
            production_set.add(Production(head, [state_to_var[start_state]]))

        for head_state, transition in transitions.items():
            for symbol, body_state in transition.items():
                prod_head = state_to_var[head_state]
                prod_body = list()

                if symbol.value == 'eps':
                    prod_body.append(Epsilon())
                elif nonterms_upper and symbol.value.isupper():
                    prod_body.append(Variable(symbol.value))
                else:
                    prod_body.append(Terminal(symbol.value))

                prod_body.append(state_to_var[body_state])
                production_set.add(Production(prod_head, prod_body))

                if body_state in enfa.final_states:
                    production_set.add(Production(
                        state_to_var[body_state], []))

        return production_set

    def from_grammar_file(path, python_regex=False, nonterms_upper=True):
        with open(path, 'r') as g:
            productions = set()

            first_line = g.readline()
            rule = first_line.strip().split(' ', 1)
            start_symbol = Variable(rule[0])
            if any(symb in rule[1] for symb in '?+*|') and len(rule[1]) > 1:
                body = rule[1].replace('?', f'| eps')
                productions |= GrammarAlgos.prod_from_regex(
                    start_symbol, body, python_regex, nonterms_upper)
            else:
                body = []
                for s in rule[1].split(' '):
                    if s == 'eps':
                        e = Epsilon()
                        body.append(e)
                    elif s.isupper():
                        v = Variable(s)
                        body.append(v)
                    else:
                        t = Terminal(s)
                        body.append(t)
                productions.add(Production(start_symbol, body))

            for line in g.readlines():
                rule = line.strip().split(' ', 1)
                var = Variable(rule[0])
                if any(symb in rule[1] for symb in '?+*|') and len(rule[1]) > 1:
                    body = rule[1].replace('?', f'| eps')
                    productions |= GrammarAlgos.prod_from_regex(
                        var, body, python_regex, nonterms_upper)
                else:
                    body = []
                    for s in rule[1].split(' '):
                        if s == 'eps':
                            e = Epsilon()
                            body.append(e)
                        elif s.isupper():
                            v = Variable(s)
                            body.append(v)
                        else:
                            t = Terminal(s)
                            body.append(t)
                    productions.add(Production(var, body))

            return CFG(start_symbol=start_symbol, productions=productions)

    def CYK(grammar: CFG, word):
        size = len(word)
        if size == 0:
            return grammar.generate_epsilon()

        cfg = grammar.to_normal_form()
        m = [[set() for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for prod in cfg.productions:
                if prod.body == [Terminal(word[i])]:
                    m[i][i].add(prod.head)

        for i in range(size):
            for j in range(size - i):
                for k in range(i):
                    first, second = m[j][j + k], m[j + k + 1][j + i]
                    for prod in cfg.productions:
                        if (
                            len(prod.body) == 2 and prod.body[0] in first and
                            prod.body[1] in second
                        ):
                            m[j][j + i].add(prod.head)

        return cfg.start_symbol in m[0][size - 1]

    def Hellings(grammar: CFG, graph: BMGraph):
        res = dict()
        m = deque()
        terminal_prods = set()
        nonterminal_prods = set()

        if grammar.generate_epsilon():
            matrix = Matrix.sparse(
                BOOL, graph.states_amount, graph.states_amount)
            for i in range(graph.states_amount):
                matrix[i, i] = True
                m.append((grammar.start_symbol, i, i))
            res[grammar.start_symbol] = matrix

        cfg = grammar.to_normal_form()

        for prod in cfg.productions:
            if len(prod.body) == 1:
                terminal_prods.add(prod)
            else:
                nonterminal_prods.add(prod)

        with semiring.LOR_LAND_BOOL:
            for t, matrix in graph.matrices.items():
                for prod in terminal_prods:
                    if prod.body == [Terminal(t)]:
                        if prod.head not in res:
                            res[prod.head] = matrix.dup()
                        else:
                            res[prod.head] += matrix.dup()

        for var, matrix in res.items():
            for i, j, _ in zip(*matrix.to_lists()):
                m.append((var, i, j))

        while m:
            add_to_res = list()
            var, v_from, v_to = m.popleft()

            for new_var, matrix in res.items():
                for new_from, _ in matrix[:, v_from]:
                    for prod in nonterminal_prods:
                        if (
                            len(prod.body) == 2 and prod.body[0] == new_var and
                            prod.body[1] == var and
                            (prod.head not in res or res[prod.head].get(
                                new_from, v_to) is None)
                        ):
                            m.append((prod.head, new_from, v_to))
                            add_to_res.append((prod.head, new_from, v_to))

            for new_var, matrix in res.items():
                for new_to, _ in matrix[v_to, :]:
                    for prod in nonterminal_prods:
                        if (
                            len(prod.body) == 2 and prod.body[0] == var and
                            prod.body[1] == new_var and
                            (prod.head not in res or res[prod.head].get(
                                v_from, new_to) is None)
                        ):
                            m.append((prod.head, v_from, new_to))
                            add_to_res.append((prod.head, v_from, new_to))

            for var, v_from, v_to in add_to_res:
                matrix = res.get(var, Matrix.sparse(
                    BOOL, graph.states_amount, graph.states_amount))
                matrix[v_from, v_to] = True
                res[var] = matrix

        return res.get(cfg.start_symbol, Matrix.sparse(
            BOOL, graph.states_amount, graph.states_amount))

    def cfpq_matrix_multiplication(grammar: CFG, graph: BMGraph):
        res = dict()
        terminal_prods = set()
        nonterminal_prods = set()

        if grammar.generate_epsilon():
            matrix = Matrix.sparse(
                BOOL, graph.states_amount, graph.states_amount)
            for i in range(graph.states_amount):
                matrix[i, i] = True
            res[grammar.start_symbol] = matrix

        cfg = grammar.to_normal_form()

        for prod in cfg.productions:
            if len(prod.body) == 1:
                terminal_prods.add(prod)
            else:
                nonterminal_prods.add(prod)

        with semiring.LOR_LAND_BOOL:
            for t, matrix in graph.matrices.items():
                for prod in terminal_prods:
                    if prod.body == [Terminal(t)]:
                        if prod.head not in res:
                            res[prod.head] = matrix.dup()
                        else:
                            res[prod.head] += matrix.dup()

        with semiring.LOR_LAND_BOOL:
            old_changed = set()
            new_changed = cfg.variables

            while len(new_changed) > 0:
                old_changed = new_changed
                new_changed = set()

                for prod in nonterminal_prods:
                    if prod.body[0] not in res or prod.body[1] not in res:
                        continue

                    if (
                        prod.body[0] in old_changed
                        or prod.body[1] in old_changed
                    ):
                        matrix = res.get(prod.head, Matrix.sparse(
                            BOOL, graph.states_amount, graph.states_amount))
                        old_nvals = matrix.nvals
                        res[prod.head] = matrix + \
                            (res[prod.body[0]] @ res[prod.body[1]])

                        if (res[prod.head].nvals != old_nvals):
                            new_changed.add(prod.head)

        return res.get(cfg.start_symbol, Matrix.sparse(
            BOOL, graph.states_amount, graph.states_amount))

    def cfpq_tensor_product(grammar: CFG, graph: BMGraph):
        res = graph.dup()

        rfa = BMGraph()
        rfa_heads = dict()

        rfa.states_amount = sum(
            [len(prod.body) + 1 for prod in grammar.productions])
        rfa.states = set(range(rfa.states_amount))
        index = 0
        for prod in grammar.productions:
            start_state = index
            final_state = index + len(prod.body)

            rfa.start_states.add(start_state)
            rfa.final_states.add(final_state)
            rfa_heads[(start_state, final_state)] = prod.head.value

            for var in prod.body:
                matrix = rfa.matrices.get(var.value, Matrix.sparse(
                    BOOL, rfa.states_amount, rfa.states_amount))

                matrix[index, index + 1] = True
                rfa.matrices[var.value] = matrix
                index += 1

            index += 1

        for prod in grammar.productions:
            if len(prod.body) == 0:
                matrix = Matrix.sparse(
                    BOOL, graph.states_amount, graph.states_amount)

                for i in range(graph.states_amount):
                    matrix[i, i] = True

                res.matrices[prod.head] = matrix

        is_changing = True
        while is_changing:
            is_changing = False
            intersection = rfa.intersect(res)
            closure = intersection.transitive_closure()

            for i, j, _ in zip(*closure.to_lists()):
                rfa_from, rfa_to = i // res.states_amount, j // res.states_amount
                graph_from, graph_to = i % res.states_amount, j % res.states_amount

                if (rfa_from, rfa_to) not in rfa_heads:
                    continue

                var = rfa_heads[(rfa_from, rfa_to)]

                matrix = res.matrices.get(var, Matrix.sparse(
                    BOOL, graph.states_amount, graph.states_amount))

                if matrix.get(graph_from, graph_to) is None:
                    is_changing = True
                    matrix[graph_from, graph_to] = True
                    res.matrices[var] = matrix

        return res.matrices.get(grammar.start_symbol, Matrix.sparse(
            BOOL, graph.states_amount, graph.states_amount))
