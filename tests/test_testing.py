from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from boar.__init__ import NOTEBOOK_PATH_00


@pytest.mark.ut
@patch("boar.testing.run_notebook")
def test_get_notebook_error_calls_functions_in_order(
    mock_run_notebook,
) -> None:
    # Given
    from boar.testing import get_notebook_error
    notebook_path = Path(NOTEBOOK_PATH_00, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_run_notebook, "mock_run_notebook")
    mock_run_notebook.return_value = None
    expected_function_calls = [
        call.mock_run_notebook(notebook_path, verbose),
    ]

    # When
    error_type, error_msg = get_notebook_error(
        notebook_path=notebook_path,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert (error_type, error_msg) == (expected_error_type, expected_error_msg)


@pytest.mark.ut
@patch("boar.testing.get_notebook_error")
def test_assert_notebook_error_calls_functions_in_order(
    mock_get_notebook_error,
) -> None:
    # Given
    from boar.testing import assert_notebook_error
    notebook_path = Path(NOTEBOOK_PATH_00, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_get_notebook_error, "mock_get_notebook_error")
    mock_get_notebook_error.return_value = (expected_error_type, expected_error_msg)
    expected_function_calls = [
        call.mock_get_notebook_error(notebook_path, verbose),
    ]

    # When
    assert_notebook_error(
        notebook_path=notebook_path,
        expected_error_type=expected_error_type,
        expected_error_msg=expected_error_msg,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls


@pytest.mark.ut
@patch("boar.testing.assert_notebook_error")
def test_check_notebook_calls_functions_in_order(
    mock_assert_notebook_error,
) -> None:
    # Given
    from boar.testing import check_notebook
    notebook_path = Path(NOTEBOOK_PATH_00, "OK.ipynb")
    expected_error_type = None
    expected_error_msg = None
    verbose = True

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_assert_notebook_error, "mock_assert_notebook_error")
    mock_assert_notebook_error.return_value = (expected_error_type, expected_error_msg)
    expected_function_calls = [
        call.mock_assert_notebook_error(
            notebook_path=notebook_path,
            expected_error_type=expected_error_type,
            expected_error_msg=expected_error_msg,
            verbose=verbose,
            ),
    ]

    # When
    check_notebook(
        notebook_path=notebook_path,
        verbose=verbose,
    )

    # Then
    assert mock_manager.mock_calls == expected_function_calls
