from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from typing import Union, List, Dict

from boar.__init__ import Tag, Notebook


@pytest.mark.ut
@pytest.mark.parametrize("notebook_path,expected_outputs", [
    (Path(Notebook._00.value, "OK.ipynb"), {}),
    (Path(Notebook.MAIN.value, "01-io-tutorial.ipynb"), {}),
    (Path(Notebook._01.value, "simple_outputs.ipynb"),
     {'outputs_1': {'b': 'B'}, 'outputs_3': {'d': 2}, 'outputs_5': {'f': 78.56}}
     ),
])
def test_run_notebook_runs_without_error(
    notebook_path: Union[str, Path],
    expected_outputs: dict,
) -> None:
    # Given
    from boar.running import run_notebook
    verbose = True

    # When
    outputs = run_notebook(
        notebook_path=notebook_path,
        verbose=verbose,
    )

    # Then
    assert outputs == expected_outputs


@pytest.mark.ut
@pytest.mark.parametrize("notebook_path,expected_cells", [
    (Path(Notebook._00.value, "OK.ipynb"), [['print("OK")']]),
    (Path(Notebook._00.value, "AssertionError.ipynb"),
     [['print("AssertionError")\n', 'assert False']]),
    (Path(Notebook._01.value, "simple_outputs.ipynb"),
     [['AAA = 0\n', 'BBB = "B"\n', 'CCC = 57\n', 'DDD = lambda x: x+1\n',
       'EEE = None\n', 'FFF = 78.56\n', 'GGG = None'],
      ['outputs_0 = {\n', '    "a" : 0\n', '}\n', '# export_start\n',
       'outputs_1 = {\n', '    "b" : BBB\n', '}\n', '# export_end\n',
       'outputs_2 = {\n', '    "c" : 2\n', '}'], ['c = 2'],
      ['"export_start"\n', 'outputs_3 = {\n', '    "d" : DDD(1)\n', '}\n',
       '"export_end"'],
      ['outputs_4 = {"e": EEE}\n', 'outputs_5 = {"f": FFF} # export_line\n',
       'outputs_6 = {"g": GGG}']]),
])
def test_get_notebook_cells_returns_correct_values(
    notebook_path: Union[str, Path],
    expected_cells: List[str],
) -> None:
    # Given
    from boar.running import get_notebook_cells

    # When
    cells = get_notebook_cells(notebook_path)

    # Then
    assert cells == expected_cells


@pytest.mark.ut
@pytest.mark.parametrize("cell,expected_compact_source", [
    (['print("OK")'], 'print("OK")'),
    (['print("AssertionError")\n', 'assert False'], 'print("AssertionError")\nassert False'),
    (['plt.show()'], "plt.draw(); plt.close('all')"),
])
def test_parse_lines_returns_correct_values(
    cell: List[List[str]],
    expected_compact_source: str,
) -> None:
    # Given
    from boar.running import parse_lines

    # When
    compact_source = parse_lines(cell)

    # Then
    assert compact_source == expected_compact_source


@patch("boar.running.split_lines_with_block_tag")
def test_split_lines_by_block_calls_functions_in_order(
    mock_split_lines_with_block_tag,
) -> None:
    # Given
    from boar.running import split_lines_by_block
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
    (f"a\nb\n#{Tag.START.value}\nc",
     [f"a\nb\n#{Tag.START.value}", f"c"]),
    (f"a\nb\n#{Tag.START.value}",
     [f"a\nb\n#{Tag.START.value}", f""]),
    (f"#{Tag.START.value}\na\nb",
     [f"#{Tag.START.value}", f"a\nb"]),
])
def test_split_lines_with_block_tag_returns_correct_values(
    source_to_split: str,
    expected_splits: List[str],
) -> None:
    # Given
    from boar.running import split_lines_with_block_tag
    start_tag = Tag.START.value

    # When
    splits = split_lines_with_block_tag(source_to_split, start_tag)

    # Then
    print(splits)
    assert splits == expected_splits


@pytest.mark.ut
@pytest.mark.parametrize("source_to_split,expected_splits", [
    (f"a", [{'code': 'a', 'export': False}]),
    (f"b #{Tag.SELECT.value}",
     [{'code': '', 'export': False},
      {'code': f'b #{Tag.SELECT.value}', 'export': True},
      {'code': '', 'export': False}]),
    (f"a\nb #{Tag.SELECT.value}\nc",
     [{'code': 'a', 'export': False},
      {'code': f'b #{Tag.SELECT.value}', 'export': True},
      {'code': 'c', 'export': False}]),
])
def test_split_lines_with_select_tag_returns_correct_value(
    source_to_split: str,
    expected_splits: List[Dict[str, Union[str, bool]]],
) -> None:
    # Given
    from boar.running import split_lines_with_select_tag
    select_tag = Tag.SELECT.value

    # When
    splits = split_lines_with_select_tag(source_to_split, select_tag)

    # Then
    assert splits == expected_splits


@pytest.mark.ut
@patch("boar.running.execute_python")
@patch("boar.running.split_lines_by_block")
def test_execute_by_block_return_correct_values(
    mock_split_lines_by_block,
    mock_execute_python,
):
    # Given
    from boar.running import execute_by_block
    compact_source = ""
    start_tag, end_tag = "", ""
    splits = [{"code": "", "export": False}]
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
@patch("boar.running.execute_python")
@patch("boar.running.split_lines_with_select_tag")
def test_execute_by_line_return_correct_values(
    mock_split_lines_with_select_tag,
    mock_execute_python,
):
    # Given
    from boar.running import execute_by_line
    compact_source = ""
    select_tag = ""
    splits = [{"code": "", "export": False}]
    expected_diffs = {}
    variables = {}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_split_lines_with_select_tag, "mock_split_lines_with_select_tag")
    mock_manager.attach_mock(mock_execute_python, "mock_execute_python")
    mock_split_lines_with_select_tag.return_value = splits
    mock_execute_python.return_value = expected_diffs
    expected_function_calls = [
        call.mock_split_lines_with_select_tag(compact_source, select_tag),
        call.mock_execute_python(splits, variables),
    ]

    # When
    diffs = execute_by_line(compact_source, select_tag, variables)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert diffs == expected_diffs


@pytest.mark.ut
@pytest.mark.parametrize("splits,expected_diffs", [
    ([{"code": "", "export": True}], {}),
    ([{"code": "a=1", "export": True}], {'a': 1}),
    ([{"code": "a=1\na=2", "export": True}], {'a': 2}),
    ([{"code": "a=1\nb=2", "export": True}], {'a': 1, 'b': 2}),
])
def test_execute_by_line_return_correct_values_2(
    splits: List[Dict[str, str]],
    expected_diffs: dict,
):
    # Given
    from boar.running import execute_python
    variables = {}
    exec("", variables)

    # When
    diffs = execute_python(splits, variables)

    # Then
    assert diffs == expected_diffs
