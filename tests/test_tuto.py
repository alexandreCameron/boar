from pathlib import Path
import pytest

from boar.__init__ import Notebook


@pytest.mark.tuto
@pytest.mark.parametrize("notebook_path", [
    Path(Notebook.MAIN.value, "00-test-tutorial.ipynb"),
    Path(Notebook.MAIN.value, "01-io-tutorial.ipynb"),
    Path(Notebook.MAIN.value, "02-lint-tutorial.ipynb"),
])
def test_tuto_runs_without_error(notebook_path: Path) -> None:
    # Given
    from boar.testing import assert_notebook
    verbose = True

    # When / Then
    assert_notebook(notebook_path, verbose)
