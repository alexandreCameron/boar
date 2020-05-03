from pathlib import Path
import json

from typing import Union, List, Dict

from boar.__init__ import BoarError


def get_code_sources(notebook_path: Union[str, Path]) -> List[List[str]]:
    return parse_ipynb(notebook_path, selection="source", projection="code")


def get_code_execution_counts(notebook_path: Union[str, Path]) -> List[List[str]]:
    return parse_ipynb(notebook_path, selection="execution_count", projection="code")


def parse_ipynb(
    notebook_path: Union[str, Path],
    selection: Union[None, str] = None,
    projection: str = "code",
) -> List[Union[List[str], Dict[str, List[str]]]]:
    with open(notebook_path, "r") as json_stream:
        content = json.load(json_stream)
    if selection is None:
        return [cell for cell in content["cells"] if cell["cell_type"] == "code"]
    if selection in ["execution_count", "metadata", "outputs", "source"]:
        return [cell[selection] for cell in content["cells"] if cell["cell_type"] == "code"]

    msg = f"{selection} is an invalid selection for notebook parsing."
    raise BoarError(msg)


def strap_source_in_one_line(cell: List[str]) -> str:
    lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
    sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
    source_to_exec = "".join(sources)
    return source_to_exec
