import json
from pathlib import Path
from sys import exc_info

from typing import Tuple, Union


def run_notebook(
    notebook_path: Union[str, Path],
    verbose: bool,
) -> None:
    """Run notebook one cell and one line at a time.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: bool
        Option to print more information
    """
    with open(notebook_path, "r") as content_file:
        content = content_file.read()
    notebook_json = json.loads(content)
    cells = [cell["source"] for cell in notebook_json["cells"] if cell["cell_type"] == "code"]

    for cell_index, cell in enumerate(cells):
        lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
        sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
        compact_source = "\n".join(sources)

        if verbose:
            print(50*"-")
            print(f"Cell {cell_index}")
            print(50*"-")
            print(compact_source)
            print("\n")
        exec(compact_source)

    try:
        exec("plt.close('all')")
    except NameError:
        print("Notebook does not use matplotlib")
        pass
    return


def get_notebook_error(
    notebook_path: Union[str, Path],
    verbose: bool,
) -> Tuple[Union[type, None], Union[str, None]]:
    """Get notebook error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: bool
        Option to print more information

    Returns
    -------
    Tuple[Union[type, None], Union[str, None]]
        error_type: class of error raised
        error_msg: error message
    """
    error_type, error_msg = None, None
    try:
        run_notebook(notebook_path, verbose)
    except (KeyboardInterrupt, Exception):
        error_type, error_msg, _ = exc_info()
    return error_type, error_msg


def assert_notebook_error(
    notebook_path: Union[str, Path],
    expected_error_type: Union[type, None],
    expected_error_msg: Union[str, None],
    verbose: bool,
) -> None:
    """Assert that notebook raise specific error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    expected_error_type : Union[type, None]
        Expected error of the notebook
    expected_error_msg : Union[str, None]
        Expected error message of the notebook
    verbose: bool
        Option to print more information
    """
    error_type, error_msg = get_notebook_error(notebook_path, verbose)
    assert error_type == expected_error_type

    if (error_type is None) or (expected_error_msg is None):
        return
    assert str(error_msg) == str(expected_error_msg)


def check_notebook(
    notebook_path: Union[str, Path],
    verbose: bool,
) -> None:
    """Check that notebook runs without error.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: bool
        Option to print more information
    """
    assert_notebook_error(
        notebook_path=notebook_path,
        expected_error_type=None,
        expected_error_msg=None,
        verbose=verbose,
    )
