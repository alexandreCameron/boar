from pathlib import Path
import pytest

from boar.__init__ import NOTEBOOK_PATH


@pytest.mark.e2e
def test_run_notebook_exports_params() -> None:
    # Given
    from boar.testing import check_notebook
    notebook_path = Path(NOTEBOOK_PATH, "01-io-tutorial.ipynb")
    verbose = True

    # When / Then
    check_notebook(notebook_path, verbose)
