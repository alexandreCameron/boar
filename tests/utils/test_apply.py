from pathlib import Path

import pytest
from unittest.mock import patch, call, Mock

from typing import List

from boar.__init__ import Notebook, ErrorLabel


@pytest.mark.ut
@patch("boar.utils.apply.apply_dir")
def test_apply_notebook_call_functions_in_order_when_dir(
    mock_apply_dir,
) -> List[str]:
    # Given
    from boar.utils.apply import apply_notebook

    def func_to_apply(*args, **kwargs):
        return "path"

    error_label = ErrorLabel.LINT.value
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_files = [sub_path.as_posix()]
    recursion_level = -1001
    max_recursion = None
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_apply_dir, "mock_apply_dir")
    mock_apply_dir.return_value = expected_incorrect_files
    expected_function_calls = [
        call.mock_apply_dir(
            dir_path, func_to_apply, error_label, inline,
            verbose, recursion_level+1, max_recursion),
    ]

    # When
    incorrect_files = apply_notebook(
        dir_path, func_to_apply, error_label, inline, verbose, recursion_level
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == expected_incorrect_files


@pytest.mark.ut
@patch("boar.utils.apply.apply_notebook")
def test_apply_dir_call_functions_in_order(
    mock_apply_notebook,
) -> List[str]:
    # Given
    from boar.utils.apply import apply_dir

    def func_to_apply(*args, **kwargs):
        return "path"

    error_label = ErrorLabel.LINT.value
    dir_path = Path(Notebook._02.value, "level-1")
    sub_path = next(dir_path.iterdir())
    expected_incorrect_files = [sub_path]
    recursion_level = -1000
    max_recursion = None
    inline = False
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_apply_notebook, "mock_apply_notebook")
    mock_apply_notebook.return_value = expected_incorrect_files
    expected_function_calls = [
        call.mock_apply_notebook(
            sub_path, func_to_apply, error_label, inline,
            verbose, recursion_level, max_recursion
        ),
    ]

    # When
    incorrect_files = apply_dir(
        dir_path, func_to_apply, error_label,
        inline, verbose, recursion_level
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == expected_incorrect_files
