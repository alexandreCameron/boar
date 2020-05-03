from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from typing import Union, List

from boar.__init__ import Notebook



@pytest.mark.ut
@patch("boar.utils.parse.parse_ipynb")
@pytest.mark.parametrize("selection", [
    ("source"), ("execution_count"),
])
def test_get_funcs_calls_functions_in_order(
    mock_parse_ipynb,
    selection: str,
) -> None:
    # Given
    if selection == "source":
        from boar.utils.parse import get_code_sources as get_func
    if selection == "execution_count":
        from boar.utils.parse import get_code_execution_counts as get_func
    expected_outputs = []
    notebook_path = "my_favorite_notebook.ipynb"
    projection = "code"

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_parse_ipynb, "mock_parse_ipynb")
    mock_parse_ipynb.return_value = expected_outputs
    expected_function_calls = [
        call.mock_parse_ipynb(
            notebook_path,
            selection=selection,
            projection=projection,
        ),
    ]

    # When
    outputs = get_func(notebook_path)

    # Then
    assert mock_manager.mock_calls == expected_function_calls
    assert outputs == expected_outputs


@pytest.mark.ut
@pytest.mark.parametrize("notebook_path,expected_sources", [
    (Path(Notebook._00.value, "OK.ipynb"), [['print("OK")']]),
    (Path(Notebook._00.value, "AssertionError.ipynb"),
     [['print("AssertionError")\n', 'assert False']]),
    (Path(Notebook._01.value, "simple_outputs.ipynb"),
     [['AAA = 0\n', 'BBB = "B"\n', 'CCC = 57\n', 'DDD = lambda x: x+1\n',
       'EEE = None\n', 'FFF = 78.56\n', 'GGG = None'],
      ['outputs_0 = {\n', '    "a" : 0\n', '}\n', '# export_start\n',
       'outputs_1 = {\n', '    "b" : BBB\n', '}\n', '# export_end\n',
       'outputs_2 = {\n', '    "c" : 2\n', '}'], ['c = 2'],
      ['# export_start\n', 'outputs_3 = {\n', '    "d" : DDD(1)\n', '}\n',
       '# export_end'],
      ['outputs_4 = {"e": EEE}\n', 'outputs_5 = {"f": FFF}  # export_line\n',
       'outputs_6 = {"g": GGG}']]),
])
def test_parse_ipynb_returns_correct_values(
    notebook_path: Union[str, Path],
    expected_sources: List[str],
) -> None:
    # Given
    from boar.utils.parse import parse_ipynb
    selection = "source"
    projection = "code"

    # When
    sources = parse_ipynb(notebook_path, selection=selection, projection=projection)

    # Then
    assert sources == expected_sources


@pytest.mark.ut
@pytest.mark.parametrize("cell,expected_source_to_exec", [
    (['print("OK")'], 'print("OK")'),
    (['print("AssertionError")\n', 'assert False'], 'print("AssertionError")\nassert False'),
    (['plt.show()'], "plt.draw(); plt.close('all')"),
])
def test_strap_source_in_one_line_returns_correct_values(
    cell: List[List[str]],
    expected_source_to_exec: str,
) -> None:
    # Given
    from boar.utils.parse import strap_source_in_one_line

    # When
    source_to_exec = strap_source_in_one_line(cell)

    # Then
    assert source_to_exec == expected_source_to_exec
