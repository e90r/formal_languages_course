# Formal Languages Course

[![Build Status](https://travis-ci.com/e90r/formal_languages_course.svg?branch=assignment_8)](https://travis-ci.com/e90r/formal_languages_course)

## Assignment 1

Basic tests for `pyformlang` and `pygraphblas` libraries, CI, and repo initialization.

To install required packages you need conda ([Miniconda download link](https://docs.conda.io/en/latest/miniconda.html)).

Create testing environment:
```
conda create -q -n test-env python=3.8 pygraphblas pytest
conda activate test-env
pip3 install pyformlang 
```

And run tests from parent folder:
```
python -m pytest
```

## Assignment 2

Note: to install necessary modules and run tests, see assignment 1.

```
usage: main.py [-h] [--from VERTICES_FROM] [--to VERTICES_TO] path_to_graph path_to_regex

Intersect graph and regex, and show reachability of graph vertices

positional arguments:
  path_to_graph         Path to graph represented in 'from value to' tuples
  path_to_regex         Path to regex

optional arguments:
  -h, --help            show this help message and exit
  --from VERTICES_FROM  Optional: source vertices from graph in 'v1 v2 v3 ...' form
  --to VERTICES_TO      Optional: destination vertices from graph in 'v1 v2 v3 ...' form
```

Example: `python main.py sample_graph.txt sample_regex.txt`

## Assignment 3

Benchmarking different ways of transitive closure: squaring and multiplying by adjacency matrix.

Gained results showed that almost no difference can be found between those two algorithms.

Full results you can see at `./benchmarks/report.pdf`

## Assignment 4

CYK and Hellings CFPQ algorithms. See at `./src/GrammarAlgos.py`

## Assignment 5

Matrix multiplication and Tensor product CFPQ algorithms. See them at `./src/GrammarAlgos.py`

Note: to run all tests, see assignment 1.

## Assignment 6

Benchmarking Hellings, Matrix multiplication and Tensor product algorithms.

Full results you can see at `./benchmarks/cfpq_report.pdf`

## Assignment 7

Implemented syntax for script language for graph database. Grammar can be found in `./src/db-language/grammar.txt` file.

See README about syntax [HERE](src/db-language/readme.md).

## Assignment 8

Added ANTLR grammar for db lanbuage. Added tree DOT-file generation.

Prerequisites (install ANTLR4 and generate neccessary files, assuming you are in root directory):

```
sudo apt-get update
sudo apt-get install antlr4
pip install antlr4-python3-runtime
cd src/db-language && antlr4 -Dlanguage=Python3 -o ../ db_language.g4 && cd ../../
```

To generate DOT file:

```
usage: tree.py [-h] script dot_file

Generate DOT file with parse tree of given script

positional arguments:
  script      Path to script written in DB language
  dot_file    Path to save generated DOT file

optional arguments:
  -h, --help  show this help message and exit
```

Example: `python tree.py ./tests/data/scripts/script1.txt ./tree.dot`
