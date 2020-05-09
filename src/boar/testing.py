from pathlib import Path
from sys import exc_info

from typing import Tuple, Union

from boar.__init__ import BoarError, ErrorLabel, VERBOSE
from boar.running import run_notebook
from boar.utils.parse import check_is_notebook
from boar.utils.apply import apply_notebook

ERROR_LABEL = ErrorLabel.ASSERT.value


def assert_notebook(
    notebook_path: Union[str, Path],
    error_label: str = ERROR_LABEL,
    verbose: bool = VERBOSE,
    recursion_level: int = 0,
    max_recursion: Union[int, None] = None,
) -> None:
    """Check that notebook runs without error.

    Applied on a directory, all the notebook will be lint down to the level
    defined by `max_recursion`.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    error_label : str, optional
        Name of the error
    verbose: bool, optional
        Option to print more information, by default False
    recursion_level : int, optional
        Level of recurssion, by default 0
        Set to -1000 if you wish to avoid raising Error
    max_recursion : Union[int, None], optional
        Depth of directory to explore, by default None

    Returns
    -------
    List[str]
        Posix of notebook that failed

    Raises
    ------
    BoarError
        At list one notebook as failed, the message will list all failed notebooks
    """
    incorrect_files = apply_notebook(
        notebook_path=notebook_path,
        func_to_apply=assert_file,
        error_label=error_label,
        verbose=verbose,
        func_params={},
        recursion_level=recursion_level,
        max_recursion=max_recursion,
    )
    return incorrect_files


def assert_file(
    notebook_path: Union[str, Path],
    error_label: str = ERROR_LABEL,
    verbose: bool = VERBOSE,
) -> None:
    """Check that notebook runs without error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    error_label : str, optional
        Name of the error
    verbose: bool, optional
        Option to print more information, by default False
    """
    notebook_path = check_is_notebook(notebook_path)
    assert_error_notebook(
        notebook_path=notebook_path,
        expected_error_type=None,
        expected_error_msg=None,
        error_label=error_label,
        verbose=verbose,
    )


def assert_error_notebook(
    notebook_path: Union[str, Path],
    expected_error_type: Union[type, None],
    expected_error_msg: Union[str, None],
    error_label: str = ERROR_LABEL,
    verbose: bool = VERBOSE,
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
    error_label : str, optional
        Name of the error
    verbose: bool, optional
        Option to print more information, by default False
    """
    notebook_path = check_is_notebook(notebook_path)
    error_type, error_msg = get_error_notebook(notebook_path, verbose)
    if error_type != expected_error_type:
        msg = f"{error_label}: {error_type} != {expected_error_type}"
        raise BoarError(msg)

    if (error_type is None) or (expected_error_msg is None):
        return

    if str(error_msg) != str(expected_error_msg):
        msg = f"{error_label}: {str(error_msg)} != {str(expected_error_msg)}"
        raise BoarError(msg)


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
