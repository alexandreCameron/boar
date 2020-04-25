from pathlib import Path
import pytest
from typing import Union

from boar.__init__ import NOTEBOOK_PATH_00


@pytest.mark.e2e
def test_check_notebook_runs_without_error() -> None:
    # Given
    from boar.run import check_notebook
    notebook_path = Path(NOTEBOOK_PATH_00, "OK.ipynb")
    verbose = True

    # When / Then
    check_notebook(notebook_path, verbose)


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
def test_assert_notebook_error_can_detect_error(
    notebook_name: str,
    expected_error_type: Union[type, None],
) -> None:
    # Given
    from boar.run import assert_notebook_error
    notebook_path = Path(NOTEBOOK_PATH_00, notebook_name)
    expected_error_msg = ""
    verbose = True

    # When / Then
    assert_notebook_error(
        notebook_path=notebook_path,
        expected_error_type=expected_error_type,
        expected_error_msg=expected_error_msg,
        verbose=verbose,
    )


@pytest.mark.e2e
def test_assert_notebook_error_can_detect_error_message() -> None:
    # Given
    from boar.run import assert_notebook_error
    notebook_path = Path(NOTEBOOK_PATH_00, "ValueError-with-message.ipynb")
    error_type = ValueError
    error_msg = "message"
    verbose = True

    # When / Then
    assert_notebook_error(notebook_path, error_type, error_msg, verbose)
