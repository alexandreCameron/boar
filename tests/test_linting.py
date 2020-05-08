from pathlib import Path

import pytest
from unittest.mock import patch, call, Mock

from typing import List, Tuple

from boar.__init__ import Notebook


@pytest.mark.ut
@patch("boar.linting.lint_file")
def test_lint_notebook_call_functions_in_order_when_file(
    mock_lint_file,
) -> List[str]:
    # Given
    from boar.linting import lint_notebook
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_lint_file = sub_path
    recursion_level = -1001
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_lint_file, "mock_lint_file")
    mock_lint_file.return_value = expected_incorrect_lint_file
    expected_function_calls = [
        call.mock_lint_file(sub_path, inline, verbose),
    ]

    # When
    incorrect_lint_files = lint_notebook(
        sub_path, inline, verbose, recursion_level
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_lint_files == [expected_incorrect_lint_file]


@pytest.mark.ut
@patch("boar.linting.lint_dir")
def test_lint_notebook_call_functions_in_order_when_dir(
    mock_lint_dir,
) -> List[str]:
    # Given
    from boar.linting import lint_notebook
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_lint_files = [sub_path]
    recursion_level = -1001
    max_recursion = None
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_lint_dir, "mock_lint_dir")
    mock_lint_dir.return_value = expected_incorrect_lint_files
    expected_function_calls = [
        call.mock_lint_dir(dir_path, inline, verbose, recursion_level+1, max_recursion),
    ]

    # When
    incorrect_lint_files = lint_notebook(dir_path, inline, verbose, recursion_level)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_lint_files == expected_incorrect_lint_files


@pytest.mark.ut
@patch("boar.linting.lint_notebook")
def test_lint_dir_call_functions_in_order(
    mock_lint_notebook,
) -> List[str]:
    # Given
    from boar.linting import lint_dir
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_files = [sub_path]
    recursion_level = -1000
    max_recursion = None
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_lint_notebook, "mock_lint_notebook")
    mock_lint_notebook.return_value = expected_incorrect_files
    expected_function_calls = [
        call.mock_lint_notebook(sub_path, inline, verbose, recursion_level, max_recursion),
    ]

    # When
    incorrect_files = lint_dir(dir_path, inline, verbose, recursion_level)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == expected_incorrect_files


@pytest.mark.ut
@patch("boar.linting.remove_output")
@patch("boar.linting.log_lint")
@patch("boar.linting.get_cell_counts")
@patch("boar.linting.get_code_execution_counts")
@pytest.mark.parametrize("cell_counts,inline", [
    [(), False],
    [(1, 1), False],
    [(1, 10), False],
    [(), True],
    [(1, 1), True],
    [(1, 10), True],
])
def test_lint_file_calls_functions_in_order(
    mock_get_code_execution_counts,
    mock_get_cell_counts,
    mock_log_lint,
    mock_remove_output,
    cell_counts: List[Tuple[int, int]],
    inline: bool,
) -> None:
    # Given
    from boar.linting import lint_file
    file_path = Path("my_notebook.ipynb")
    is_incorrect_file = (cell_counts != [])
    expected_file_posix = file_path.as_posix() if is_incorrect_file else None
    counts = [None]
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_get_code_execution_counts, "mock_get_code_execution_counts")
    mock_manager.attach_mock(mock_get_cell_counts, "mock_get_cell_counts")
    mock_manager.attach_mock(mock_log_lint, "mock_log_lint")
    mock_manager.attach_mock(mock_remove_output, "mock_remove_output")
    mock_get_code_execution_counts.return_value = counts
    mock_get_cell_counts.return_value = cell_counts
    expected_function_calls = [
        call.mock_get_code_execution_counts(file_path),
        call.mock_get_cell_counts(counts)
    ]
    if is_incorrect_file:
        if inline:
            expected_function_calls.append(
                call.mock_remove_output(file_path, inline)
            )

        expected_function_calls.append(
            call.mock_log_lint(expected_file_posix, cell_counts, verbose)
        )

    # When
    file_posix = lint_file(file_path, inline, verbose)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert file_posix == expected_file_posix
