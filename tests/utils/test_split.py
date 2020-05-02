import pytest
from unittest.mock import patch, call, Mock

from typing import List, Dict, Union

from boar.__init__ import Tag


@patch("boar.utils.split.split_lines_with_block_tag")
def test_split_lines_by_block_calls_functions_in_order(
    mock_split_lines_with_block_tag,
) -> None:
    # Given
    from boar.utils.split import split_lines_by_block
    source_to_split = "012"
    start_splits = ["0", "12"]
    end_splits = ["1", "2"]
    start_tag, end_tag = "", ""
    expected_splits = [
        {"code": start_splits[0], "export": False},
        {"code": end_splits[0], "export": True},
        {"code": end_splits[1], "export": False},
    ]

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_split_lines_with_block_tag, "mock_split_lines_with_block_tag")
    mock_split_lines_with_block_tag.side_effect = [start_splits, end_splits]
    expected_function_calls = [
        call.mock_split_lines_with_block_tag(source_to_split, start_tag),
        call.mock_split_lines_with_block_tag(start_splits[1], end_tag),
    ]

    # When
    splits = split_lines_by_block(source_to_split, start_tag, end_tag)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert splits == expected_splits


@pytest.mark.ut
@pytest.mark.parametrize("source_to_split,expected_splits", [
    (f"a\nb\n#{Tag.EXPORT_START.value}\nc",
     [f"a\nb\n#{Tag.EXPORT_START.value}", f"c"]),
    (f"a\nb\n#{Tag.EXPORT_START.value}",
     [f"a\nb\n#{Tag.EXPORT_START.value}", f""]),
    (f"#{Tag.EXPORT_START.value}\na\nb",
     [f"#{Tag.EXPORT_START.value}", f"a\nb"]),
])
def test_split_lines_with_block_tag_returns_correct_values(
    source_to_split: str,
    expected_splits: List[str],
) -> None:
    # Given
    from boar.utils.split import split_lines_with_block_tag
    start_tag = Tag.EXPORT_START.value

    # When
    splits = split_lines_with_block_tag(source_to_split, start_tag)

    # Then
    print(splits)
    assert splits == expected_splits


@pytest.mark.ut
@pytest.mark.parametrize("source_to_split,expected_splits", [
    (f"a", [{'apply': False, 'code': 'a', 'type': 'export'}]),
    (f"b {Tag.EXPORT_LINE.value}",
     [{'apply': False, 'code': '', 'type': 'export'},
      {'apply': True, 'code': f'b {Tag.EXPORT_LINE.value}', 'type': 'export'},
      {'apply': False, 'code': '', 'type': 'export'}]),
    (f"a\nb {Tag.EXPORT_LINE.value}\nc",
     [{'apply': False, 'code': 'a', 'type': 'export'},
      {'apply': True, 'code': f'b {Tag.EXPORT_LINE.value}', 'type': 'export'},
      {'apply': False, 'code': 'c', 'type': 'export'}]),
])
def test_split_lines_with_line_tag_returns_correct_value(
    source_to_split: str,
    expected_splits: List[Dict[str, Union[str, bool]]],
) -> None:
    # Given
    from boar.utils.split import split_lines_with_line_tag
    line_tag = Tag.EXPORT_LINE.value

    # When
    splits = split_lines_with_line_tag(source_to_split, line_tag)

    # Then
    assert splits == expected_splits
