from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from boar.__init__ import Notebook


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
