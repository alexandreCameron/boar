# Usage

## Testing

A simple way to test your notebook is to follow the test:

```python
def test_check_notebook_runs_without_error():
    # Given
    from boar.testing import check_notebook

    # When / Then
    check_notebook("my_favorite.ipynb", verbose=True)
```

Other examples are presented at: [./tests/test_testing_e2e.py](./tests/test_testing_e2e.py)

## Running

A simple way to run a notebook is to use:

```python
from boar.running import run_notebook

outputs = run_notebook("my_favorite.ipynb")
```

The outputs can be defined in the notebook by adding `# export_line` for a line or `# export_start` and `# export_end`.

Other examples are presented in: [./notebook/01-test-tutorial.ipynb](./notebook/01-test-tutorial.ipynb)

## Caveat

1. On the graphic package `matplotlib.pyplot` as been test. Use other graphic option at your on risk

2. Only python code can be executed, donnot try to use the package on notebook with julia or R.

3. When executing a notebook via `boar` make sure the environment has all the package to run the notebook.

4. The package has not been developped to work recursively. Use at your own risk.

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
