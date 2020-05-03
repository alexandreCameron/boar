import pytest
from unittest.mock import patch, call, Mock


@pytest.mark.ut
@patch("boar.utils.log.get_logger_print")
@pytest.mark.parametrize("name,args", [
    ("execution", (1, "2")),
    ("lint", ("/my/posix/path", [(1, 2)])),
])
def test_log_execution_calls_functions_in_order(
    mock_get_logger_print,
    name: str,
    args: tuple,
) -> None:
    # Given
    if name == "execution":
        from boar.utils.log import log_execution
        log_func = log_execution
    if name == "lint":
        from boar.utils.log import log_lint
        log_func = log_lint

    def logger(x):
        return x
    verbose = False

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_get_logger_print, "mock_get_logger_print")
    mock_get_logger_print.return_value = logger
    expected_function_calls = [
        call.mock_get_logger_print(verbose),
    ]

    # When
    assert log_func(*args, verbose) is None

    # Then
    assert mock_manager.mock_calls == expected_function_calls
