from pathlib import Path
from typing import Any, List, Union
from types import FunctionType

from boar.__init__ import BoarError, VERBOSE


def apply_notebook(
    notebook_path: Union[str, Path],
    func_to_apply: FunctionType,
    error_label: str,
    verbose: Any = VERBOSE,
    func_params: dict = {},
    recursion_level: int = 0,
    max_recursion: Union[int, None] = None,
) -> List[str]:
    notebook_path = Path(notebook_path)
    incorrect_files = []

    # If max recursion
    if (max_recursion is not None) and (recursion_level >= max_recursion):
        return incorrect_files

    # If notebook
    if notebook_path.suffix == ".ipynb":
        try:
            file_posix = func_to_apply(notebook_path, error_label, verbose, **func_params)
        except BoarError:
            file_posix = Path(notebook_path).as_posix()
        incorrect_files.append(file_posix)

    # If directory
    if notebook_path.is_dir():
        incorrect_files.extend(apply_dir(
            notebook_path, func_to_apply, error_label,
            verbose, func_params, recursion_level+1, max_recursion
        ))

    incorrect_lint_files = [name for name in incorrect_files if name is not None]

    if (recursion_level != 0):
        return incorrect_lint_files

    if incorrect_lint_files == []:
        return None

    incorrect_lint_str = "\n".join(incorrect_lint_files)
    msg = f"{error_label} issues in:\n{incorrect_lint_str}"
    raise BoarError(msg)


def apply_dir(
    dir_path: Union[str, Path],
    func_to_apply: FunctionType,
    error_label: str,
    verbose: Any,
    func_params: dict,
    recursion_level: int,
    max_recursion: Union[int, None] = None,
) -> List[str]:
    dir_path = Path(dir_path)
    incorrect_files = []
    for sub_path in sorted(dir_path.iterdir()):
        if sub_path.name == ".ipynb_checkpoints":
            continue
        if sub_path.is_dir() or sub_path.suffix == ".ipynb":
            incorrect_subs = apply_notebook(
                sub_path, func_to_apply, error_label,
                verbose, func_params, recursion_level, max_recursion
            )
            incorrect_files.extend(incorrect_subs)
    return incorrect_files
