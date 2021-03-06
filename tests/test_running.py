import pytest
from unittest.mock import patch, call, Mock


@pytest.mark.ut
@patch("boar.running.close_plots")
@patch("boar.running.get_code_sources")
@patch("boar.running.check_is_notebook")
def test_run_notebook_calls_functions_in_order(
    mock_check_is_notebook,
    mock_get_code_sources,
    mock_close_plots,
) -> None:
    # Given
    from boar.running import run_notebook
    from boar.__init__ import Notebook
    notebook_path = next(Notebook._00.value.iterdir())
    sources = []
    expected_outputs = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_check_is_notebook, "mock_check_is_notebook")
    mock_manager.attach_mock(mock_get_code_sources, "mock_get_code_sources")
    mock_manager.attach_mock(mock_close_plots, "mock_close_plots")
    mock_check_is_notebook.return_value = notebook_path
    mock_get_code_sources.return_value = sources
    expected_function_calls = [
        call.mock_check_is_notebook(notebook_path),
        call.mock_get_code_sources(notebook_path),
        call.mock_close_plots(),
    ]

    # When
    diffs = run_notebook(notebook_path)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert diffs == expected_outputs
