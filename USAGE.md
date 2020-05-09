# Usage

## Testing

To test your notebook follow:

```python
def test_assert_notebook_runs_without_error():
    # Given
    from boar.testing import assert_notebook

    # When / Then
    assert_notebook("my_favorite.ipynb", verbose=True)
```

Other examples are presented at: [./tests/test_testing_e2e.py](https://github.com/alexandreCameron/boar/blob/master/tests/test_testing_e2e.py)

---

## Linting

If plots are drawn in notebooks, it is not recommended to commit them to the repo.
Therefore, `boar` considers notebook-linting as making sure no data is saved in the notebooks.
The function is designed to raise an error when outputs have not been clear.
The error will indicate the notebook and the cells at fault.

To lint a notebook (or recursively on all notebooks in a directory), use:

```python
from boar.linting import lint_notebook
lint_notebook("my_favorite.ipynb", inline=False, verbose=True)
```

```python
from boar.linting import lint_notebook
lint_notebook("my_notebook_directory", inline=False, verbose=True)
```

If the `inline` option is set to `True`, a linted verion of the the notebook will be saved.
This version will have `outputs = []` and `execution_count = NOne`.

Other examples are presented at: [./notebook/02-lint-tutorial.ipynb](https://github.com/alexandreCameron/boar/blob/master/notebook/02-lint-tutorial.ipynb)

---

## Running

### Synthax

To run a notebook use:

```python
from boar.running import run_notebook

outputs = run_notebook("my_favorite.ipynb", inputs={"a": 1}, verbose=True)
```

### Export

The outputs are defined in the notebook by adding

* `# export_line` for a line
* `# export_start` and `# export_end` for a block.

Examples are presented at: [./notebook/01-test-tutorial.ipynb](https://github.com/alexandreCameron/boar/blob/master/notebook/01-io-tutorial.ipynb)

### Skip

Section of the notebook can be skip using the keywords:

* `# skip_line` for a line
* `# skip_start` and `# skip_end` for a block.

### Inputs

Inputs variables can be execute before the notebook using the `inputs` parameter of the `run_notebook` function.

Combined with the skip option, inputs allow run a notebook for differents parameters.

### Example

If a variable in a notebook is defined as:

```python
data_file = "my_data_file.csv"  # skip_line
```

and an input dictionary defined as:

```python
inputs = {"data_file": "data_file_1.csv"}
```

The skip option will prevent the code from executing `data_file = "my_data_file.csv"`.

The input parameter will set `data_file = "data_file_1.csv"`.

This is not the best way to put code in production but it can help out in some occasions.

---

## Caveats

### Limits

* Only the graphic package `matplotlib.pyplot` as been tested. Other graphic package may not give back the hand.

* Only python code can be executed. The package will **not** work on julia or R notebooks.

* When executing a notebook via `boar` make sure the environment has all the package to run the notebook.

* The package has not been developped to work recursively. Do not execute boar on notebooks that execute boar on other notebooks!

### Forbidden synthax

Some synthax used in notebook can **not** be used with `boar`:

* Magic command starting with `%%`, `!` or any command that cannot be used in a python file.

Use `import pip ; pip.main(["install", "my-package"])`, to install package within the notebook instead of `! pip install my-package`

* Variable, list, dictionary comprehension.

```python
# This synthax will **fail**
b = [a for a in range(10) if a > 3]
```

```python
# This synthax will **pass**
b = []
for a in range(10):
    if a > 3:
        b.append(a)
```

* Function calls for functions defined within the notebook scope.

```python
# This synthax will **fail**
def f2(a):
    return a**2

def f2plus1(a):
    return f2(a) +1
```

```python
# This synthax will **pass**
def f2plus1(a):
    def f2(a):
        return a**2
    return f2(a) +1
```

* Package imports in the notebook scope.

```python
# This synthax will **fail**
import numpy as np

def f2plus1(a):
    return np.square(a) +1
```

```python
# This synthax will **pass**
def f2plus1(a):
    import numpy as np
    return np.square(a) +1
```

* Use of `export` or `skip` tags in a indented section.
