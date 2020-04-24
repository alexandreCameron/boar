import pytest

from pathlib import Path

from boar.__init__ import NOTEBOOK_PATH
from boar.run import run_notebook


@pytest.mark.tuto
@pytest.mark.filterwarnings("ignore", category=RuntimeWarning)
@pytest.mark.parametrize("notebook_name,expected_outcome", [
    ("00-OK.ipynb", True),
    ("00-KO.ipynb", False),
    ])
def test_run_notebook_can_detect_error(notebook_name: str, expected_outcome: bool) -> None:
    # Given
    notebook_path = Path(NOTEBOOK_PATH, notebook_name)

    # When
    try:
        run_notebook(notebook_path)
        outcome = True
    except SystemExit:
        outcome = False

    # Then
    assert outcome == expected_outcome
