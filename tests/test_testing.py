from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from boar.__init__ import Notebook, ErrorLabel

ERROR_LABEL = ErrorLabel.ASSERT.value


@pytest.mark.ut
@patch("boar.testing.assert_file")
@patch("boar.testing.apply_notebook")
def test_assert_notebook_calls_functions_in_order(
    mock_apply_notebook,
    mock_assert_file,
) -> None:
    # Given
    from boar.testing import assert_notebook
    notebook_path = Path(Notebook._00.value, "Assertion.ipynb")
    expected_incorrect_files = [notebook_path.as_posix()]
    error_label = ERROR_LABEL
    verbose = True
    recursion_level = 0
    max_recursion = None
    func_params = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_apply_notebook, "mock_apply_notebook")
    mock_apply_notebook.return_value = expected_incorrect_files
    expected_function_calls = [
        call.mock_apply_notebook(
            notebook_path=notebook_path,
            func_to_apply=mock_assert_file,
            error_label=error_label,
            verbose=verbose,
            func_params=func_params,
            recursion_level=recursion_level,
            max_recursion=max_recursion,
        )
    ]

    # When
    incorrect_files = assert_notebook(
        notebook_path=notebook_path,
        error_label=error_label,
        verbose=verbose,
        recursion_level=recursion_level,
        max_recursion=max_recursion,
    )

    # Then
    print(incorrect_files)
    assert mock_manager.mock_calls == expected_function_calls
    assert incorrect_files == expected_incorrect_files


@pytest.mark.ut
@patch("boar.testing.assert_error_notebook")
@patch("boar.testing.check_is_notebook")
def test_assert_file_calls_functions_in_order(
    mock_check_is_notebook,
    mock_assert_error_notebook,
) -> None:
    # Given
    from boar.testing import assert_file
    notebook_path = Path(Notebook._00.value, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    error_label = ERROR_LABEL
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_check_is_notebook, "mock_check_is_notebook")
    mock_manager.attach_mock(mock_assert_error_notebook, "mock_assert_error_notebook")
    mock_check_is_notebook.return_value = notebook_path
    mock_assert_error_notebook.return_value = (expected_error_type, expected_error_msg)
    expected_function_calls = [
        call.mock_check_is_notebook(notebook_path),
        call.mock_assert_error_notebook(
            notebook_path=notebook_path,
            expected_error_type=expected_error_type,
            expected_error_msg=expected_error_msg,
            error_label=error_label,
            verbose=verbose,
            ),
    ]

    # When
    assert_file(
        notebook_path=notebook_path,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls


@pytest.mark.ut
@patch("boar.testing.get_error_notebook")
@patch("boar.testing.check_is_notebook")
def test_assert_error_notebook_calls_functions_in_order(
    mock_check_is_notebook,
    mock_get_error_notebook,
) -> None:
    # Given
    from boar.testing import assert_error_notebook
    notebook_path = Path(Notebook._00.value, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    error_label = ERROR_LABEL
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_check_is_notebook, "mock_check_is_notebook")
    mock_manager.attach_mock(mock_get_error_notebook, "mock_get_error_notebook")
    mock_check_is_notebook.return_value = notebook_path
    mock_get_error_notebook.return_value = (expected_error_type, expected_error_msg)
    expected_function_calls = [
        call.mock_check_is_notebook(notebook_path),
        call.mock_get_error_notebook(notebook_path, verbose),
    ]

    # When
    assert_error_notebook(
        notebook_path=notebook_path,
        expected_error_type=expected_error_type,
        expected_error_msg=expected_error_msg,
        error_label=error_label,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls


@pytest.mark.ut
@patch("boar.testing.run_notebook")
def test_get_error_notebook_calls_functions_in_order(
    mock_run_notebook,
) -> None:
    # Given
    from boar.testing import get_error_notebook
    notebook_path = Path(Notebook._00.value, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_run_notebook, "mock_run_notebook")
    mock_run_notebook.return_value = None
    expected_function_calls = [
        call.mock_run_notebook(notebook_path, verbose=verbose),
    ]

    # When
    error_type, error_msg = get_error_notebook(
        notebook_path=notebook_path,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert (error_type, error_msg) == (expected_error_type, expected_error_msg)
