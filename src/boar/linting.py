from pathlib import Path
from typing import Any, List, Union

from boar.__init__ import BoarError
from boar.utils.log import log_lint
from boar.utils.parse import get_code_execution_counts, remove_output


def lint_notebook(
    notebook_path: Union[str, Path],
    inline: bool,
    verbose: Any,
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
        incorrect_files.append(lint_file(notebook_path, inline, verbose))

    # If directory
    if notebook_path.is_dir():
        incorrect_files.extend(lint_dir(
            notebook_path, inline, verbose, recursion_level+1, max_recursion
        ))

    incorrect_lint_files = [name for name in incorrect_files if name is not None]

    if (recursion_level != 0):
        return incorrect_lint_files

    if incorrect_lint_files == []:
        return None

    incorrect_lint_str = "\n".join(incorrect_lint_files)
    msg = f"Linting issues in:\n{incorrect_lint_str}"
    raise BoarError(msg)


def lint_dir(
    dir_path: Union[str, Path],
    inline: bool,
    verbose: Any,
    recursion_level: int,
    max_recursion: Union[int, None] = None,
) -> List[str]:
    dir_path = Path(dir_path)
    incorrect_files = []
    for sub_path in sorted(dir_path.iterdir()):
        if sub_path.name == ".ipynb_checkpoints":
            continue
        if sub_path.is_dir() or sub_path.suffix == ".ipynb":
            incorrect_subs = lint_notebook(
                sub_path, inline, verbose, recursion_level, max_recursion
            )
            incorrect_files.extend(incorrect_subs)
    return incorrect_files


def lint_file(
    file_path: Union[str, Path],
    inline: bool,
    verbose: Any
) -> Union[None, str]:
    file_path = Path(file_path)
    counts = get_code_execution_counts(file_path)
    cell_counts = get_cell_counts(counts)
    if cell_counts == []:
        return None

    if inline:
        remove_output(file_path, inline)

    file_posix = Path(file_path).as_posix()
    log_lint(file_posix, cell_counts, verbose)
    return file_posix


def get_cell_counts(counts):
    return [(idx+1, count) for idx, count in enumerate(counts) if count is not None]
