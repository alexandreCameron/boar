# Usage

## Using `boar` for notebook test

A simple way to test your notebook is to follow the test:

```python
def test_check_notebook_runs_without_error() -> None:
    # Given
    from boar.testing import check_notebook
    notebook_path = Path(NOTEBOOK_PATH, "my_favorite.ipynb")
    verbose = True

    # When / Then
    check_notebook(notebook_path, verbose)
```

Other tests are presented at: [./tests/test_run_e2e.py](./tests/test_run_e2e.py)

## Caveat

1. On the graphic package `matplotlib.pyplot` as been test. Use other graphic option at your on risk

2. Only python code can be executed, donnot try to use the package on notebook with julia or R.

3. When executing a notebook via `boar` make sure the environment has all the package to run the notebook.

## Forbidden synthax

Some synthax used in notebook can **not** be used with `boar`:

1. Magic command starting with `%%`, `!` or any command that cannot be used in a python file.

2. Variable, list, dictionary comprehension.

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
