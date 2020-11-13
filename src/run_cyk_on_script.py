from src.GrammarAlgos import GrammarAlgos


keywords = {
    'connect', 'select', 'from', 'grammar', 'setStartAndFinal', 'e', 'count',
    'edges', 'filter', 'hasLbl', 'isStart', 'isFinal', 'term', 'nonterm',
    '"', '(', ')', ':', '&', '[', ']', '{', '}',
    ',', '->', '.', '+', '?', '|', '*', '_', '!'
}


def prepare_script(script):
    res = list()
    script = script.replace('\n', ' ')
    for s in ['"', '(', ')', ':', '&', '[', ']', '{', '}',
              ',', '->', '.', '+', '?', '|', '*', '_', '!']:
        script = script.replace(s, f' {s} ')
    for w in script.split():
        if w in keywords:
            res.append(w)
        else:
            res.extend(w)
    return res


def run_cyk_on_script(script):
    grammar = GrammarAlgos.from_grammar_file(
        'src/db-language/grammar.txt', python_regex=True, nonterms_upper=False)
    script_prepared = prepare_script(script)
    return GrammarAlgos.CYK(grammar, script_prepared)
