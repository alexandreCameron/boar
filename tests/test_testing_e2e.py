from pathlib import Path
import pytest
from typing import Union

from boar.__init__ import Notebook


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.e2e
@pytest.mark.parametrize("notebook_name", [
    "OK.ipynb",
    "Matplotlib.ipynb",
])
def test_assert_notebook_runs_without_error(notebook_name) -> None:
    # Given
    from boar.testing import assert_notebook
    notebook_path = Path(Notebook._00.value, notebook_name)
    verbose = True

    # When / Then
    assert_notebook(notebook_path, verbose)


@pytest.mark.e2e
@pytest.mark.parametrize("notebook_name,expected_error_type", [
    ("OK.ipynb", None),
    ("AssertionError.ipynb", AssertionError),
    ("Exception.ipynb", Exception),
    ("ImportError.ipynb", ImportError),
    ("IndexError.ipynb", IndexError),
    ("KeyboardInterrupt.ipynb", KeyboardInterrupt),
    ("KeyError.ipynb", KeyError),
    ("ModuleNotFoundError.ipynb", ModuleNotFoundError),
    ("NameError.ipynb", NameError),
    ("StopIteration.ipynb", StopIteration),
    ("TypeError.ipynb", TypeError),
    ("ValueError.ipynb", ValueError),
    ("ZeroDivisionError.ipynb", ZeroDivisionError),
])
def test_assert_error_notebook_detects_error(
    notebook_name: str,
    expected_error_type: Union[type, None],
) -> None:
    # Given
    from boar.testing import assert_error_notebook
    notebook_path = Path(Notebook._00.value, notebook_name)
    expected_error_msg = ""
    verbose = True

    # When / Then
    assert_error_notebook(
        notebook_path=notebook_path,
        expected_error_type=expected_error_type,
        expected_error_msg=expected_error_msg,
        verbose=verbose,
    )


@pytest.mark.e2e
def test_assert_error_notebook_detects_error_message() -> None:
    # Given
    from boar.testing import assert_error_notebook
    notebook_path = Path(Notebook._00.value, "ValueError-with-message.ipynb")
    error_type = ValueError
    error_msg = "message"
    verbose = True

    # When / Then
    assert_error_notebook(notebook_path, error_type, error_msg, verbose)


@pytest.mark.e2e
def test_tuto_runs_without_error() -> None:
    # Given
    from boar.testing import assert_notebook
    notebook_path = Path(Notebook.MAIN.value, "00-test-tutorial.ipynb")
    verbose = True

    # When / Then
    assert_notebook(notebook_path, verbose)
