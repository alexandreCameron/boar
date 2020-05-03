from pathlib import Path
from typing import Any, List, Union

from boar.__init__ import BoarError
from boar.utils.log import log_lint
from boar.utils.parse import get_code_execution_counts


def lint_notebook(
    notebook_path: Path,
    verbose: Any,
    recursion_level: int = 0,
) -> List[str]:
    incorrect_files = []

    # If notebook
    if notebook_path.suffix == ".ipynb":
        incorrect_files.append(lint_file(notebook_path, verbose))

    # If directory
    if notebook_path.is_dir():
        incorrect_files.extend(lint_dir(notebook_path, verbose, recursion_level+1))

    incorrect_lint_files = [name for name in incorrect_files if name is not None]

    if (recursion_level != 0):
        return incorrect_lint_files

    if incorrect_lint_files == []:
        return None

    incorrect_lint_str = "\n".join(incorrect_lint_files)
    msg = f"Linting issues in:\n{incorrect_lint_str}"
    raise BoarError(msg)


def lint_dir(
    dir_path: Path,
    verbose: Any,
    recursion_level: int,
) -> List[str]:
    incorrect_files = []
    for sub_path in sorted(dir_path.iterdir()):
        if sub_path.name == ".ipynb_checkpoints":
            continue
        if sub_path.is_dir() or sub_path.suffix == ".ipynb":
            incorrect_subs = lint_notebook(sub_path, verbose, recursion_level)
            incorrect_files.extend(incorrect_subs)
    return incorrect_files


def lint_file(file_path: Path, verbose: Any) -> Union[None, str]:
    counts = get_code_execution_counts(file_path)
    cell_counts = get_cell_counts(counts)
    if cell_counts == []:
        return None

    file_posix = Path(file_path).as_posix()
    log_lint(file_posix, cell_counts, verbose)
    return file_posix


def get_cell_counts(counts):
    return [(idx+1, count) for idx, count in enumerate(counts) if count is not None]
