# Formal Languages Course

## Assignment 1

[![Build Status](https://travis-ci.org/e90r/formal_languages_course.svg?branch=assignment_1)](https://travis-ci.org/e90r/formal_languages_course)

Basic tests for `pyformlang` and `pygraphblas` libraries, CI, and repo initialization.

To install required packages you need conda ([Miniconda download link](https://docs.conda.io/en/latest/miniconda.html)).

Create testing environment:
```
conda create -q -n test-env python=3.8 pygraphblas pytest
conda activate test-env
pip3 install pyformlang 
```

And run tests:
```
pytest tests.py
```