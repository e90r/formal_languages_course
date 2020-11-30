from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from .db_languageLexer import db_languageLexer
from .db_languageParser import db_languageParser


class AntlrParser():
    def __init__(self, path=None):
        self.path = path
        if self.path is not None:
            self.stream = FileStream(self.path)
        else:
            self.stream = StdinStream()

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
        if self.__parse() is not None:
            return True
        else:
            return False


class DefaultErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception
