from pathlib import Path

import pytest
from unittest.mock import patch, call, Mock

from typing import List, Tuple

from boar.__init__ import BoarError, Notebook, ErrorLabel


@pytest.mark.ut
@patch("boar.linting.lint_file")
def test_lint_notebook_call_functions_in_order_when_file(
    mock_lint_file,
) -> List[str]:
    # Given
    from boar.linting import lint_notebook
    error_label = ErrorLabel.LINT.value
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_file = sub_path
    recursion_level = -1001
    inline = False
    verbose = True

    print(sub_path)
    print(expected_incorrect_file)

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_lint_file, "mock_lint_file")
    mock_lint_file.return_value = expected_incorrect_file
    expected_function_calls = [
        call.mock_lint_file(sub_path, error_label, inline, verbose),
    ]

    # When
    incorrect_files = lint_notebook(
        sub_path, inline, verbose, recursion_level
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == [expected_incorrect_file]


@pytest.mark.ut
@patch("boar.linting.lint_file")
@patch("boar.linting.apply_notebook")
def test_lint_notebook_call_functions_in_order_when_dir(
    mock_apply_notebook,
    mock_lint_file,
) -> List[str]:
    # Given
    from boar.linting import lint_notebook
    error_label = ErrorLabel.LINT.value
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_files = [sub_path]
    recursion_level = -1001
    max_recursion = None
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_apply_notebook, "mock_apply_notebook")
    mock_manager.attach_mock(mock_lint_file, "mock_lint_file")
    mock_apply_notebook.return_value = expected_incorrect_files
    expected_function_calls = [
        call.mock_apply_notebook(
            notebook_path=dir_path,
            func_to_apply=mock_lint_file,
            error_label=error_label,
            inline=inline,
            verbose=verbose,
            recursion_level=recursion_level,
            max_recursion=max_recursion,
        ),
    ]

    # When
    incorrect_files = lint_notebook(dir_path, inline, verbose, recursion_level)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == expected_incorrect_files


@pytest.mark.ut
@patch("boar.linting.log_lint")
@patch("boar.linting.remove_output")
@patch("boar.linting.get_cell_counts")
@patch("boar.linting.get_code_execution_counts")
@pytest.mark.parametrize("cell_counts,inline", [
    ([], False),
    ([(1, 1)], False),
    ([(1, 10)], False),
    ([], True),
    ([(1, 1)], True),
    ([(1, 10)], True),
])
def test_lint_file_calls_functions_in_order(
    mock_get_code_execution_counts,
    mock_get_cell_counts,
    mock_remove_output,
    mock_log_lint,
    cell_counts: List[Tuple[int, int]],
    inline: bool,
) -> None:
    # Given
    from boar.linting import lint_file
    file_path = next(Path(Notebook._02.value, "level-1").iterdir())
    is_incorrect_file = (cell_counts != [])
    error_label = ErrorLabel.LINT.value
    file_posix = file_path.as_posix()
    expected_msg = None
    if is_incorrect_file:
        expected_msg = f"{error_label}: {file_posix}"
        if inline:
            expected_msg = f"{file_posix}"
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
        expected_function_calls.append(
            call.mock_log_lint(file_posix, cell_counts, verbose)
        )
        if inline:
            expected_function_calls.append(
                call.mock_remove_output(file_path, inline)
            )

    # When
    try:
        msg = lint_file(file_path, error_label, inline, verbose)
    except BoarError as err:  # noqa
        msg = str(err)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert msg == expected_msg
