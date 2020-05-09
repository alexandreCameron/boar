from pathlib import Path
from typing import Any, List, Union

from boar.__init__ import BoarError, ErrorLabel, VERBOSE, INLINE
from boar.utils.apply import apply_notebook
from boar.utils.log import log_lint
from boar.utils.parse import (
    get_code_execution_counts, get_cell_counts, remove_output, check_is_notebook
)

ERROR_LABEL = ErrorLabel.LINT.value


def lint_notebook(
    notebook_path: Union[str, Path],
    error_label: str = ERROR_LABEL,
    verbose: Any = VERBOSE,
    inline: bool = INLINE,
    recursion_level: int = 0,
    max_recursion: Union[int, None] = None,
) -> List[str]:
    """Lint notebook.

    Applied on a directory, all the notebook will be lint down to the level
    defined by `max_recursion`.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Notebook path or notebook directory
    error_label : str, optional
        Name of the error
    verbose : Any, optional
        Verbosity option, by default True
    inline : bool, optional
        Replace existing notebook with linted version, by default False
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
        func_to_apply=lint_file,
        error_label=ERROR_LABEL,
        verbose=verbose,
        func_params={"inline": inline},
        recursion_level=recursion_level,
        max_recursion=max_recursion,
    )
    return incorrect_files


def lint_file(
    file_path: Union[str, Path],
    error_label: str = ERROR_LABEL,
    verbose: Any = VERBOSE,
    inline: bool = INLINE,
) -> Union[None, str]:
    """Lints one file.

    Parameters
    ----------
    file_path : Union[str, Path]
        Päth of the notebook, must be file
    error_label : str, optional
        Name of the error
    verbose : Any, optional
        Verbosity optional
    inline : bool,optional
        Replace existing notebook with linted version

    Returns
    -------
    Union[None, str]
        Path in posix format if notebook fail else None

    Raises
    ------
    BoarError
        Notebook is not a file or not linted.
    """
    file_path = check_is_notebook(file_path)
    counts = get_code_execution_counts(file_path)
    cell_counts = get_cell_counts(counts)
    if cell_counts == []:
        return None

    file_posix = Path(file_path).as_posix()
    log_lint(file_posix, cell_counts, verbose)

    if inline:
        remove_output(file_path, inline)
        return file_posix

    msg = f"{error_label}: {file_posix}"
    raise BoarError(msg)
