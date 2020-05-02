from pathlib import Path
import pytest

from typing import Union, List

from boar.__init__ import Notebook


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
      ['# export_start\n', 'outputs_3 = {\n', '    "d" : DDD(1)\n', '}\n',
       '# export_end'],
      ['outputs_4 = {"e": EEE}\n', 'outputs_5 = {"f": FFF}  # export_line\n',
       'outputs_6 = {"g": GGG}']]),
])
def test_get_notebook_cells_returns_correct_values(
    notebook_path: Union[str, Path],
    expected_cells: List[str],
) -> None:
    # Given
    from boar.utils.parse import get_notebook_cells

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
    from boar.utils.parse import parse_lines

    # When
    compact_source = parse_lines(cell)

    # Then
    assert compact_source == expected_compact_source
