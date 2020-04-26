from pathlib import Path
import pytest

from boar.__init__ import NOTEBOOK_PATH_00


@pytest.mark.ut
def test_run_notebook_runs_without_error() -> None:
    # Given
    from boar.testing import run_notebook
    notebook_path = Path(NOTEBOOK_PATH_00, "OK.ipynb")
    verbose = True

    # When / Then
    run_notebook(
        notebook_path=notebook_path,
        verbose=verbose,
    )
