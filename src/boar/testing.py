from pathlib import Path
from sys import exc_info

from typing import Tuple, Union

from boar.__init__ import BoarError
from boar.running import run_notebook
from boar.utils.parse import check_is_notebook


def get_error_notebook(
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
        _ = run_notebook(notebook_path, verbose=verbose)
    except (KeyboardInterrupt, Exception):
        error_type, error_msg, _ = exc_info()
    return error_type, error_msg


def assert_error_notebook(
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
    error_type, error_msg = get_error_notebook(notebook_path, verbose)
    if error_type != expected_error_type:
        msg = f"{error_type} != {expected_error_type}"
        raise BoarError(msg)

    if (error_type is None) or (expected_error_msg is None):
        return

    if str(error_msg) != str(expected_error_msg):
        msg = f"{str(error_msg)} != {str(expected_error_msg)}"
        raise BoarError(msg)


def assert_notebook(
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
    assert_file(notebook_path, verbose)


def assert_file(
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
    notebook_path = check_is_notebook(notebook_path)
    assert_error_notebook(
        notebook_path=notebook_path,
        expected_error_type=None,
        expected_error_msg=None,
        verbose=verbose,
    )
