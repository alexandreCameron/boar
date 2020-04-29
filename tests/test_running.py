from pathlib import Path
import pytest

from typing import Union

from boar.__init__ import Notebook


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


# @pytest.mark.ut
# @pytest.mark.parametrize("notebook_name,expected_error_type", [
#     (Path("OK.ipynb") , None),
# ])
# def test_get_notebook_cells_returns_correct_value(
#     notebook_path: Union[str, Path]
# ) -> None:
#     with open(notebook_path, "r") as json_stream:
#         content = json.load(json_stream)
#     cells = [cell["source"] for cell in content["cells"] if cell["cell_type"] == "code"]
#     return cells
