from pathlib import Path
import json

from typing import Union, List, Dict

from boar.__init__ import BoarError


def get_cell_counts(counts):
    return [(idx+1, count) for idx, count in enumerate(counts) if count is not None]


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
    sources = []
    for line in lines:
        line_no_space = line.replace(" ", "")
        if line_no_space.startswith("%"):
            continue
        if line_no_space.startswith("!"):
            continue
        sources.append(line)
    source_to_exec = "".join(sources)
    return source_to_exec


def remove_output(file_path: Union[str, Path], inline: bool) -> Union[Dict, None]:
    with open(file_path, "r") as json_stream:
        content = json.load(json_stream)

    cleaned_content = {}
    cleaned_content["cells"] = [clean_cell(cell) for cell in content["cells"]]
    cleaned_content.update({key: value for key, value in content.items() if key != "cells"})

    if inline:
        with open(file_path, "w+") as json_stream:
            json.dump(cleaned_content, json_stream, indent=1)
        return
    return cleaned_content


def clean_cell(cell: dict):
    if cell["cell_type"] != "code":
        return cell

    cleaned_cell = {
        key: value for key, value in cell.items()
        if key not in ["execution_count", "outputs"]
    }
    cleaned_cell["execution_count"] = None
    cleaned_cell["outputs"] = []
    return cleaned_cell
