# boar

Dirty tricks to run python notebooks

![test](https://github.com/alexandreCameron/boar/workflows/test/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/)

## Purpose

Testing an idea is sometimes more easily done by calling a python notebook in a python code.
It is practice as dirty, filthy and ugly as a boar...
But if you can prove the value of your idea, why not trying it out.

## Practice

I used this trick in CI jobs to make sure tutorials associated to a project stay up-to-date.

I would not recommend to use this code on a deployed product.

## Usage

### Using `boar` for notebook test

A simple way to test your notebook is to follow the test:

```python
def test_check_notebook_runs_without_error() -> None:
    # Given
    from boar.run import check_notebook
    notebook_path = Path(NOTEBOOK_PATH, "my_favorite.ipynb")
    verbose = True

    # When / Then
    check_notebook(notebook_path, verbose)
```

Other tests are presented at: [./tests/test_run_e2e.py](./tests/test_run_e2e.py)

### Forbidden synthax

Some synthax used in notebook can **not** be used with `boar`:

1. Magic command starting with `%%`

2. Variable, list, dictionary comprehension. (eg: ``)

    This synthax will **fail**:

    ```python
    b = [a for a in range(10) if a > 3]
    ```

    This synthax will **pass**:

    ```python
    b = []
    for a in range(10):
        if a > 3:
            b.append(a)
    ```

3. Function calls for functions defining in the notebook scope.

    This synthax will **fail**:

    ```python
    def f2(a):
        return a**2

    def f2plus1(a):
        return f2(a) +1
    ```

    This synthax will **pass**:

    ```python
    def f2plus1(a):
        def f2(a):
            return a**2
        return f2(a) +1
    ```

4. Package imports in the notebook scope.

    This synthax will **fail**:

    ```python
    import numpy as np

    def f2plus1(a):
        return np.square(a) +1
    ```

    This synthax will **pass**:

    ```python
    def f2plus1(a):
        import numpy as np
        return np.square(a) +1
    ```
