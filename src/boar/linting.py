from pathlib import Path
from typing import Any, List

from boar.__init__ import BoarError
from boar.utils.log import log_lint
from boar.utils.parse import get_code_execution_counts


def lint_notebook(
    notebook_path: Path,
    verbose: Any,
    recursion_level: int = 0,
) -> List[str]:
    incorrect_lint_files = []

    # If notebook
    if notebook_path.suffix == ".ipynb":
        counts = get_code_execution_counts(notebook_path)
        cell_counts = [(idx+1, count) for idx, count in enumerate(counts) if count is not None]
        if cell_counts != []:
            file_posix = notebook_path.as_posix()
            incorrect_lint_files.append(file_posix)
            log_lint(file_posix, cell_counts, verbose)

    # If directory
    if notebook_path.is_dir():
        for sub_path in sorted(notebook_path.iterdir()):
            if sub_path.name == ".ipynb_checkpoints":
                continue
            if sub_path.is_dir() or sub_path.suffix == ".ipynb":
                incorrect_files = lint_notebook(sub_path, verbose, recursion_level+1)
                incorrect_lint_files.extend(incorrect_files)

    if (recursion_level != 0):
        return incorrect_lint_files

    if incorrect_lint_files == []:
        return None

    incorrect_lint_str = "\n".join(incorrect_lint_files)
    msg = f"Linting issues in:\n{incorrect_lint_str}"
    raise BoarError(msg)
