from pathlib import Path
import json

from typing import Union, List, Dict

from boar.__init__ import BoarError


def parse_sources(notebook_path: Union[str, Path]) -> List[List[str]]:
    return parse_codes(notebook_path, key="source")


def parse_codes(
    notebook_path: Union[str, Path],
    key=None,
) -> List[Union[List[str], Dict[str, List[str]]]]:
    with open(notebook_path, "r") as json_stream:
        content = json.load(json_stream)
    if key is None:
        return [cell for cell in content["cells"] if cell["cell_type"] == "code"]
    if key in ["execution_count", "metadata", "outputs", "source"]:
        return [cell[key] for cell in content["cells"] if cell["cell_type"] == "code"]
    else: 
        msg = f"{key} is an invalid key for notebook parsing."
        raise BoarError(msg)


def strap_source_in_one_line(cell: List[str]) -> str:
    lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
    sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
    source_to_exec = "".join(sources)
    return source_to_exec
