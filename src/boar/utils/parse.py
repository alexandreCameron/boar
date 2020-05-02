from pathlib import Path
import json

from typing import Union, List


def get_notebook_cells(notebook_path: Union[str, Path]) -> List[List[str]]:
    with open(notebook_path, "r") as json_stream:
        content = json.load(json_stream)
    cells = [cell["source"] for cell in content["cells"] if cell["cell_type"] == "code"]
    return cells


def parse_lines(cell: List[str]) -> str:
    lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
    sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
    compact_source = "".join(sources)
    return compact_source
