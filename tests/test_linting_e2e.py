from pathlib import Path
from sys import exc_info

import pytest

from typing import List

from boar.__init__ import Notebook, BoarError


@pytest.mark.parametrize("notebook_path,expected_incorrect_lint_files", [
    (Path(Notebook._02.value, "0-execution.ipynb"), []),
    (Notebook._02.value, [
        '/home/alex/Desktop/github/boar/notebook/02-lint/1-execution.ipynb',
        '/home/alex/Desktop/github/boar/notebook/02-lint/level-1/one-execution.ipynb',
        '/home/alex/Desktop/github/boar/notebook/02-lint/unstructured-executions.ipynb',
     ]
     ),
])
def test_lint_notebook_returns_correct_values(
    notebook_path: Path,
    expected_incorrect_lint_files: List[str],
):
    # Given
    from boar.linting import lint_notebook
    verbose = False
    recursion_level = -1000

    # When
    incorrect_lint_files = lint_notebook(
        notebook_path,
        verbose=verbose,
        recursion_level=recursion_level
    )

    # Then
    print(incorrect_lint_files)

    assert incorrect_lint_files == expected_incorrect_lint_files


def test_lint_notebook_returns_error_when_fail():
    # Given
    from boar.linting import lint_notebook
    error_msg = "Incorrect error message"
    expected_error_msg = (
        f"Linting issues in:\n" +
        f"/home/alex/Desktop/github/boar/notebook/02-lint/1-execution.ipynb\n" +
        f"/home/alex/Desktop/github/boar/notebook/02-lint/level-1/one-execution.ipynb\n" +
        f"/home/alex/Desktop/github/boar/notebook/02-lint/unstructured-executions.ipynb"
    )

    # When
    try:
        lint_notebook(Notebook._02.value, verbose=False)
    except BoarError:
        _, error_msg, _ = exc_info()
        pass

    # Then
    assert str(error_msg) == expected_error_msg
