from src.run_cyk_on_script import run_cyk_on_script


def test_correct_syntax():
    script = '''
    connect "/home/egor"
    select edges from "graph"
    '''
    assert run_cyk_on_script(script)

    script = '''
    S : nonterm(S).term(a).nonterm(S).term(b)
    S : e
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from ("graph" && grammar)
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from (setStartAndFinal 0:6 {1,3,4} "graph")
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from (setStartAndFinal _ _ "graph")
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from (setStartAndFinal _ _ ("graph" && grammar))
    '''
    assert run_cyk_on_script(script)

    script = '''
    select filter (v, e, u) -> (e hasLbl abc) : edges from "graph"
    '''
    assert run_cyk_on_script(script)

    script = '''
    select filter (v, e, u) -> (e hasLbl abc & isStart v | !(isFinal u)) : edges from "graph"
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from [term(a)?.term(b)*.(term(c)|term(d))+]
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from ("graph" && [term(a).term(b)*.(term(c)|term(d))+])
    '''
    assert run_cyk_on_script(script)

    script = '''
    select count edges from ("graph1" && ("graph2" && "graph3"))
    '''
    assert run_cyk_on_script(script)

    script = '''
    select edges from [((term(a)))]
    '''
    assert run_cyk_on_script(script)

    script = ''
    assert run_cyk_on_script(script)


def test_wrong_syntax():
    script = '''
    select count count edges from "graph"
    '''
    assert not run_cyk_on_script(script)

    script = '''
    select count edges from (setStartAndFinal string string "graph")
    '''
    assert not run_cyk_on_script(script)

    script = '''
    select edges from [((term(a))]
    '''
    assert not run_cyk_on_script(script)
