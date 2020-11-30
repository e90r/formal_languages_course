import os
from src.AntlrParser import AntlrParser


def test_script_1():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script1.txt')
    assert AntlrParser(test_path).check()


def test_script_2():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script2.txt')
    assert AntlrParser(test_path).check()


def test_script_3():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script3.txt')
    assert AntlrParser(test_path).check()


def test_script_4():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script4.txt')
    assert AntlrParser(test_path).check()


def test_script_5():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script5.txt')
    assert AntlrParser(test_path).check()


def test_script_6():
    test_path = os.path.join(os.getcwd(), 'tests/data/scripts/script6.txt')
    assert AntlrParser(test_path).check()


def test_wrong_script_1():
    test_path = os.path.join(
        os.getcwd(), 'tests/data/scripts/wrong_script1.txt')
    assert not AntlrParser(test_path).check()


def test_wrong_script_2():
    test_path = os.path.join(
        os.getcwd(), 'tests/data/scripts/wrong_script2.txt')
    assert not AntlrParser(test_path).check()
