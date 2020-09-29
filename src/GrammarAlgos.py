from collections import deque

from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL
from src.BMGraph import BMGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG


class GrammarAlgos:
    def from_grammar_file(path):
        with open(path, 'r') as g:
            vars = set()
            terminals = set()
            productions = set()

            first_line = g.readline()
            rule = first_line.replace('\n', '').split(' ')
            start_symbol = Variable(rule[0])
            vars.add(start_symbol)
            body = []
            if len(rule) > 1:
                for s in rule[1:]:
                    if s.islower():
                        t = Terminal(s)
                        terminals.add(t)
                        body.append(t)
                    else:
                        v = Variable(s)
                        vars.add(v)
                        body.append(v)

            productions.add(Production(start_symbol, body))

            for line in g.readlines():
                rule = line.replace('\n', '').split(' ')
                var = rule[0]
                vars.add(var)
                body = []
                if len(rule) > 1:
                    for s in rule[1:]:
                        if s.islower():
                            t = Terminal(s)
                            terminals.add(t)
                            body.append(t)
                        else:
                            v = Variable(s)
                            vars.add(v)
                            body.append(v)

                productions.add(Production(var, body))

            return CFG(vars, terminals, start_symbol, productions)

    def CYK(grammar: CFG, word: str):
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

        if grammar.generate_epsilon():
            matrix = Matrix.sparse(
                BOOL, graph.states_amount, graph.states_amount)
            for i in range(graph.states_amount):
                matrix[i, i] = True
                m.append((grammar.start_symbol, i, i))
            res[grammar.start_symbol] = matrix

        cfg = grammar.to_normal_form()

        for t, matrix in graph.matrices.items():
            for prod in cfg.productions:
                if prod.body == [Terminal(t)]:
                    res[prod.head] = matrix

        for var, matrix in res.items():
            for i, j, _ in zip(*matrix.to_lists()):
                m.append((var, i, j))

        while m:
            add_to_res = list()
            var, v_from, v_to = m.popleft()

            for new_var, matrix in res.items():
                for new_from, _ in matrix[:, v_from]:
                    for prod in cfg.productions:
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
                    for prod in cfg.productions:
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
