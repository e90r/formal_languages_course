from src.db_languageListener import db_languageListener
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees
from .db_languageLexer import db_languageLexer
from .db_languageParser import db_languageParser


class AntlrDBGrammarParser():
    def __init__(self, path=None):
        self.path = path
        if self.path is not None:
            self.stream = FileStream(self.path)
        else:
            self.stream = StdinStream()
        self.tree = self.__parse()

    def __parse(self):
        lexer = db_languageLexer(self.stream)
        token_stream = CommonTokenStream(lexer)
        parser = db_languageParser(token_stream)
        parser.addErrorListener(DefaultErrorListener())

        try:
            return parser.script()
        except Exception:
            return None

    def check(self):
        return self.tree is not None

    def generate_dot_tree(self, path):
        if self.tree is None:
            raise Exception('Parse tree was not generated')

        traverser = TreeTraverser(db_languageParser)
        traverser.traverse(self.tree)

        with open(path, 'w+') as dot_tree:
            dot_tree.write('digraph script {\n')
            for (index, label) in traverser.nodes:
                raw_label = '\\' + label if label == '\"' else label
                dot_tree.write(f'\t{index} [label="{raw_label}"];\n')
            dot_tree.write('\n')
            for (node_from, node_to) in traverser.edges:
                dot_tree.write(f'\t{node_from} -> {node_to};\n')
            dot_tree.write('}')


class DefaultErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception


class TreeTraverser():
    def __init__(self, parser):
        self.parser = parser
        self.cnt = 0
        self.stack = [0]
        self.edges = []
        self.nodes = []

    def traverse(self, tree):
        parent_label = Trees.getNodeText(tree, self.parser.ruleNames)
        self.nodes.append((self.stack[-1], parent_label))
        for child in Trees.getChildren(tree):
            self.cnt += 1
            self.edges.append((self.stack[-1], self.cnt))
            self.stack.append(self.cnt)
            self.traverse(child)
            self.stack.pop()
