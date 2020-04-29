from pathlib import Path
from sys import exc_info

from typing import Tuple, Union

from boar.running import run_notebook


def get_notebook_error(
    notebook_path: Union[str, Path],
    verbose: bool,
) -> Tuple[Union[type, None], Union[str, None]]:
    """Get notebook error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: bool, optional
        Option to print more information, by default False

    Returns
    -------
    Tuple[Union[type, None], Union[str, None]]
        error_type: class of error raised
        error_msg: error message
    """
    error_type, error_msg = None, None
    try:
        _ = run_notebook(notebook_path, verbose)
    except (KeyboardInterrupt, Exception):
        error_type, error_msg, _ = exc_info()
    return error_type, error_msg


def assert_notebook_error(
    notebook_path: Union[str, Path],
    expected_error_type: Union[type, None],
    expected_error_msg: Union[str, None],
    verbose: bool,
) -> None:
    """Assert that notebook raise specific error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    expected_error_type : Union[type, None]
        Expected error of the notebook
    expected_error_msg : Union[str, None]
        Expected error message of the notebook
    verbose: bool, optional
        Option to print more information, by default False
    """
    error_type, error_msg = get_notebook_error(notebook_path, verbose)
    print(error_type, error_msg)
    assert error_type == expected_error_type

    if (error_type is None) or (expected_error_msg is None):
        return
    assert str(error_msg) == str(expected_error_msg)


def check_notebook(
    notebook_path: Union[str, Path],
    verbose: bool,
) -> None:
    """Check that notebook runs without error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: bool, optional
        Option to print more information, by default False
    """
    assert_notebook_error(
        notebook_path=notebook_path,
        expected_error_type=None,
        expected_error_msg=None,
        verbose=verbose,
    )
