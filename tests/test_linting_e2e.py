from pathlib import Path
from sys import exc_info

import pytest

from typing import List

from boar.__init__ import Notebook, BoarError


@pytest.mark.e2e
@pytest.mark.parametrize("notebook_path,expected_incorrect_lint_files", [
    (Path(Notebook._02.value, "0-execution.ipynb"), []),
    (Notebook._02.value, [
        "notebook/02-lint/1-execution.ipynb",
        "notebook/02-lint/level-1/one-execution.ipynb",
        "notebook/02-lint/unstructured-executions.ipynb",
     ]),
    (Notebook._00.value, [])
])
def test_lint_notebook_returns_correct_values(
    notebook_path: Path,
    expected_incorrect_lint_files: List[str],
):
    # Given
    from boar.linting import lint_notebook
    inline = False
    verbose = False
    recursion_level = -1000

    # When
    incorrect_lint_files = lint_notebook(
        notebook_path,
        inline=inline,
        verbose=verbose,
        recursion_level=recursion_level
    )

    # TODO Parse message to remove str up to notebook part
    parsed_incorrect_lint_files = []
    for fname in incorrect_lint_files:
        parsed_name = []
        for part in reversed(Path(fname).parts):
            parsed_name.append(part)
            if part == "notebook":
                break
        parsed_incorrect_lint_files.append(Path(*parsed_name[::-1]).as_posix())

    # Then
    assert parsed_incorrect_lint_files == expected_incorrect_lint_files


@pytest.mark.e2e
def test_lint_notebook_returns_error_when_fail():
    # Given
    from boar.linting import lint_notebook
    error_msg = "Incorrect error message"
    expected_error_msg = (
        f"Linting issues in:\n" +
        f"notebook/02-lint/1-execution.ipynb\n" +
        f"notebook/02-lint/level-1/one-execution.ipynb\n" +
        f"notebook/02-lint/unstructured-executions.ipynb"
    )
    inline = False
    verbose = False

    # When
    try:
        lint_notebook(Notebook._02.value, inline=inline, verbose=verbose)
    except BoarError:
        _, error_msg, _ = exc_info()
        pass

    # TODO Parse message to remove str up to notebook part
    parsed_error_lines = []
    for line in str(error_msg).split("\n"):
        if "notebook" in line:
            parsed_error_lines.append("notebook" + line.split("notebook")[1])
        else:
            parsed_error_lines.append(line)
    parsed_error_msg = "\n".join(parsed_error_lines)

    # Then
    assert parsed_error_msg == expected_error_msg
