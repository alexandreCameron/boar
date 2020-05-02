import pytest
from unittest.mock import patch, call, Mock

from typing import List, Dict, Any


@pytest.mark.ut
@patch("boar.utils.execute.execute_python")
@patch("boar.utils.execute.split_lines_by_block")
def test_execute_by_block_return_correct_values(
    mock_split_lines_by_block,
    mock_execute_python,
):
    # Given
    from boar.utils.execute import execute_by_block
    compact_source = ""
    start_tag, end_tag = "", ""
    splits = [{"code": "", "type": "export", "apply": False}]
    expected_diffs = {}
    variables = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_split_lines_by_block, "mock_split_lines_by_block")
    mock_manager.attach_mock(mock_execute_python, "mock_execute_python")
    mock_split_lines_by_block.return_value = splits
    mock_execute_python.return_value = expected_diffs
    expected_function_calls = [
        call.mock_split_lines_by_block(compact_source, start_tag, end_tag),
        call.mock_execute_python(splits, variables),
    ]

    # When
    diffs = execute_by_block(compact_source, start_tag, end_tag, variables)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert diffs == expected_diffs


@pytest.mark.ut
@patch("boar.utils.execute.execute_python")
@patch("boar.utils.execute.split_lines_with_line_tag")
def test_execute_by_line_return_correct_values(
    mock_split_lines_with_line_tag,
    mock_execute_python,
):
    # Given
    from boar.utils.execute import execute_by_line
    compact_source = ""
    line_tag = ""
    splits = [{"code": "", "type": "export", "apply": False}]
    expected_diffs = {}
    variables = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_split_lines_with_line_tag, "mock_split_lines_with_line_tag")
    mock_manager.attach_mock(mock_execute_python, "mock_execute_python")
    mock_split_lines_with_line_tag.return_value = splits
    mock_execute_python.return_value = expected_diffs
    expected_function_calls = [
        call.mock_split_lines_with_line_tag(compact_source, line_tag),
        call.mock_execute_python(splits, variables),
    ]

    # When
    diffs = execute_by_line(compact_source, line_tag, variables)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert diffs == expected_diffs


@pytest.mark.ut
@patch("boar.utils.execute.get_dict_diff")
@patch("boar.utils.execute.make_special")
@pytest.mark.parametrize("export", [True, False])
def test_execute_python_call_functions_in_order(
    mock_make_special,
    mock_get_dict_diff,
    export: bool,
):
    # Given
    from boar.utils.execute import execute_python
    variables = {}
    splits = [{"code": "a=1", "type": "export", "apply": export}]
    __VeRyYyY_sPecIAl_temp = {}
    __VeRyYyY_sPecIAl_vars = {"a": 1}
    diff = {"a": 1}
    if export:
        expected_diffs = {**diff}
    else:
        expected_diffs = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_make_special, "mock_make_special")
    mock_manager.attach_mock(mock_get_dict_diff, "mock_get_dict_diff")
    mock_make_special.side_effect = [__VeRyYyY_sPecIAl_temp, __VeRyYyY_sPecIAl_vars]
    mock_get_dict_diff.return_value = diff
    if export:
        expected_function_calls = [
            call.mock_make_special(variables),
            call.mock_make_special(variables),
            call.mock_get_dict_diff(__VeRyYyY_sPecIAl_vars, __VeRyYyY_sPecIAl_temp),
        ]
    else:
        expected_function_calls = []

    # When
    diffs = execute_python(splits, variables)

    # Then
    assert diffs == expected_diffs
    assert mock_manager.mock_calls == expected_function_calls


@pytest.mark.ut
@pytest.mark.parametrize("splits,expected_diffs", [
    ([{"code": "", "type": "export", "apply": True}], {}),
    ([{"code": "a=1", "type": "export", "apply": True}], {'a': 1}),
    ([{"code": "a=1\na=2", "type": "export", "apply": True}], {'a': 2}),
    ([{"code": "a=1\nb=2", "type": "export", "apply": True}], {'a': 1, 'b': 2}),
])
def test_execute_python_return_correct_values(
    splits: List[Dict[str, str]],
    expected_diffs: dict,
):
    # Given
    from boar.utils.execute import execute_python
    variables = {}

    # When
    diffs = execute_python(splits, variables)

    # Then
    assert diffs == expected_diffs


@pytest.mark.ut
@pytest.mark.parametrize("a_dict,expected_diff", [
    ({"a": 1}, {"a": 1}),
    ({"__VeRyYyY_sPecIAl_a": 1}, {}),
    ({"a": 1, "__VeRyYyY_sPecIAl_a": 1}, {"a": 1})
])
def test_make_special_return_correct_values(
    a_dict: Dict[str, Any],
    expected_diff: dict,
):
    # Given
    from boar.utils.execute import make_special

    # When
    diff = make_special(a_dict)

    # Then
    assert diff == expected_diff


@pytest.mark.ut
@pytest.mark.parametrize("a_dict,b_dict,expected_diff", [
    ({"a": 1}, {}, {"a": 1}),
    ({"a": 1}, {"a": 1}, {}),
    ({"a": 2}, {"a": 1}, {"a": 2}),
    ({"a": 1, "b": 2}, {"a": 1}, {"b": 2}),
])
def test_get_dict_diff_return_correct_values(
    a_dict: dict,
    b_dict: dict,
    expected_diff: dict,
):
    # Given
    from boar.utils.execute import get_dict_diff

    # When
    diff = get_dict_diff(a_dict, b_dict)

    # Then
    assert diff == expected_diff
