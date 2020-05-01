from pathlib import Path
import pytest

from typing import Union

from boar.__init__ import Notebook


@pytest.mark.e2e
@pytest.mark.parametrize("notebook_path,expected_outputs", [
    (Path(Notebook._00.value, "OK.ipynb"), {}),
    (Path(Notebook.MAIN.value, "01-io-tutorial.ipynb"), {}),
    (Path(Notebook._01.value, "simple_outputs.ipynb"),
     {'outputs_1': {'b': 'B'}, 'outputs_3': {'d': 2}, 'outputs_5': {'f': 78.56}}
     ),
])
def test_run_notebook_exports_params(
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


@pytest.mark.e2e
def test_tuto_runs_without_error() -> None:
    # Given
    from boar.testing import check_notebook
    notebook_path = Path(Notebook.MAIN.value, "01-io-tutorial.ipynb")
    verbose = True

    # When / Then
    check_notebook(notebook_path, verbose)
