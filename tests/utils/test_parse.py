from pathlib import Path
import pytest
from unittest.mock import patch, call, Mock

from typing import Union, List, Tuple

from boar.__init__ import Notebook


@pytest.mark.ut
@pytest.mark.parametrize("counts,expected_cell_counts", [
    ([None], []),
    ([None, None, None], []),
    ([None, 3, None], [(2, 3)]),

])
def test_get_cell_counts_returns_correct_values(
    counts: List[Union[None, int]],
    expected_cell_counts: List[Tuple[int, int]],
) -> None:
    # Given
    from boar.utils.parse import get_cell_counts

    # When
    cell_counts = get_cell_counts(counts)

    # Then
    assert cell_counts == expected_cell_counts


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
        from boar.utils.parse import get_code_sources
        get_func = get_code_sources
    if selection == "execution_count":
        from boar.utils.parse import get_code_execution_counts
        get_func = get_code_execution_counts
    expected_outputs = []
    notebook_path = Path("my_favorite_notebook.ipynb")
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


@pytest.mark.ut
@patch("boar.utils.parse.clean_cell")
def test_remove_output_returns_correct_values(
    mock_clean_cell
) -> None:
    # Given
    from boar.utils.parse import remove_output
    from boar.__init__ import Notebook
    file_path = Path(Notebook._02.value, "0-execution.ipynb")
    inline = False
    cells = [
        {'cell_type': 'code', 'execution_count': None, 'metadata': {},
         'outputs': [], 'source': ['a = 1\n', 'print(a)']},
        {'cell_type': 'markdown', 'metadata': {}, 'source': ['---']}]
    cleaned_cells = [
        {'cell_type': 'code', 'metadata': {},
         'source': ['a = 1\n', 'print(a)'], 'execution_count': None, 'outputs': []},
        {'cell_type': 'markdown', 'metadata': {}, 'source': ['---']}]
    not_cells = {
        'metadata': {
            'kernelspec': {
                'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
            'language_info': {
                'codemirror_mode': {'name': 'ipython', 'version': 3},
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.8.0'}
            },
        'nbformat': 4,
        'nbformat_minor': 4

    }
    expected_cleaned_content = {'cells': cleaned_cells, **not_cells}

    # Thus
    mock_manager = Mock()
    mock_manager.attach_mock(mock_clean_cell, "mock_clean_cell")
    mock_clean_cell.side_effect = cleaned_cells
    expected_function_calls = [
        call.mock_clean_cell(cells[0]),
        call.mock_clean_cell(cells[1]),
    ]

    # When
    cleaned_content = remove_output(file_path, inline)

    # Then
    print(cells)
    assert mock_manager.mock_calls == expected_function_calls
    assert cleaned_content == expected_cleaned_content


@pytest.mark.ut
@pytest.mark.parametrize("cell,expected_cleaned_cell", [
    ({"cell_type": "not_code"}, {"cell_type": "not_code"}),
    ({"cell_type": "code"},
     {"cell_type": "code", 'execution_count': None, 'outputs': []}),
    ({"cell_type": "code", 'execution_count': 1, 'outputs': ["a"]},
     {"cell_type": "code", 'execution_count': None, 'outputs': []}),
])
def test_clean_cell_returns_correct_values(
    cell: dict,
    expected_cleaned_cell: dict,
) -> None:
    # Given
    from boar.utils.parse import clean_cell

    # When
    cleaned_cell = clean_cell(cell)

    # Then
    assert cleaned_cell == expected_cleaned_cell
