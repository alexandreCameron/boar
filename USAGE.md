# Usage

## Testing

A simple way to test your notebook is to follow the test:

```python
def test_assert_notebook_runs_without_error():
    # Given
    from boar.testing import assert_notebook

    # When / Then
    assert_notebook("my_favorite.ipynb", verbose=True)
```

Other examples are presented at: [./tests/test_testing_e2e.py](https://github.com/alexandreCameron/boar/blob/master/tests/test_testing_e2e.py)

---

## Running

### Synthax

A simple way to run a notebook is to use:

```python
from boar.running import run_notebook

outputs = run_notebook("my_favorite.ipynb", inputs={"a": 1}, verbose=True)
```

### Export

The outputs are defined in the notebook by adding

* `# export_line` for a line
* `# export_start` and `# export_end` for a block.

Other examples are presented in: [./notebook/01-test-tutorial.ipynb](https://github.com/alexandreCameron/boar/blob/master/notebook/01-io-tutorial.ipynb)

### Skip

Section of the notebook can be skip using the keywords:

* `# skip_line` for a line
* `# skip_start` and `# skip_end` for a block.

### Inputs

Inputs variables can be execute before the notebook using the `inputs` parameter of the `run_notebook` function.

Combined with the skip option, inputs allow run a notebook for differents parameters.

### Example

If you have a variable in you notebook defined as:

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

* Only the graphic package `matplotlib.pyplot` as been tested. Use other graphic option at your on risk.

* Only python code can be executed, donnot try to use the package on notebook with julia or R.

* When executing a notebook via `boar` make sure the environment has all the package to run the notebook.

* The package has not been developped to work recursively. Use at your own risk.

### Forbidden synthax

Some synthax used in notebook can **not** be used with `boar`:

* Magic command starting with `%%`, `!` or any command that cannot be used in a python file.

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
