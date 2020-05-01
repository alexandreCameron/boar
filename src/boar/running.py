import json
from pathlib import Path

from typing import List, Union, Dict

from boar.__init__ import Tag, BoarError, EXCEPTION_KEYS
from boar.utils.log import (log_execution, close_plots)
from copy import deepcopy


def run_notebook(
    notebook_path: Union[str, Path],
    inputs: dict = {},
    verbose: Union[bool, object] = False,
    start_tag: str = Tag.EXPORT_START.value,
    end_tag: str = Tag.EXPORT_END.value,
    select_tag: str = Tag.EXPORT_LINE.value,
) -> None:
    """Run notebook one cell and one line at a time.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    verbose: Union[bool, object], optional
        Option to print more information, by default False
    """
    # Parse json
    cells = get_notebook_cells(notebook_path)

    # Run set new inputs
    locals().update(inputs)

    # Run Code
    outputs = {}
    for cell_index, cell in enumerate(cells):
        # Parse cell lines for execution
        compact_source = parse_lines(cell)
        log_execution(cell_index, compact_source, verbose=verbose)

        # Run, if no export tag
        if (start_tag in compact_source) and (select_tag in compact_source):
            msg = f"`{start_tag}` and `{select_tag}` cannot be in same cell."
            raise BoarError(msg)

        if start_tag in compact_source:
            diffs = execute_by_block(compact_source, start_tag, end_tag, locals())
            outputs.update(diffs)
            continue

        if select_tag in compact_source:
            diffs = execute_by_line(compact_source, select_tag, locals())
            outputs.update(diffs)
            continue

        exec(compact_source)

    close_plots()
    return deepcopy(outputs)


# Parsing

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


# Split

def split_lines_by_block(
    source_to_split: str,
    start_tag: str,
    end_tag: str,
) -> List[Dict[str, Union[str, bool]]]:
    start_splits = split_lines_with_block_tag(source_to_split, start_tag)
    end_splits = split_lines_with_block_tag(start_splits[1], end_tag)

    splits = [
        {"code": start_splits[0], "export": False},
        {"code": end_splits[0], "export": True},
        {"code": end_splits[1], "export": False},
    ]
    return splits


def split_lines_with_block_tag(
    source_to_split: str,
    tag: str,
) -> List[str]:
    block_splits, block = [], []
    for line in source_to_split.split("\n"):
        block.append(line)
        if tag in line:
            block_splits.append("\n".join(block))
            block = []
            continue
    block_splits.append("\n".join(block))

    if len(block_splits) > 2:
        msg = f"Multiple `{tag}` in:\n{source_to_split}"
        raise BoarError(msg)
    return block_splits


def split_lines_with_select_tag(
    source_to_split: str,
    tag: str,
) -> List[Dict[str, Union[str, bool]]]:
    splits, block = [], []
    for line in source_to_split.split("\n"):
        if tag in line:
            splits.append({"code": "\n".join(block), "export": False})
            splits.append({"code": line, "export": True})
            block = []
            continue
        block.append(line)
    splits.append({"code": "\n".join(block), "export": False})
    return splits


# Execution

def execute_by_block(compact_source: str, start_tag: str, end_tag: str, variables: dict) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    splits = split_lines_by_block(compact_source, start_tag, end_tag)
    return execute_python(splits, variables)


def execute_by_line(compact_source: str, select_tag: str, variables: dict) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    splits = split_lines_with_select_tag(compact_source, select_tag)
    return execute_python(splits, variables)


def execute_python(
    splits: List[Dict[str, Union[str, bool]]],
    variables: dict
) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    diffs = {}
    for split in splits:
        if split["export"]:
            __VeRyYyY_sPecIAl_temp = make_special(variables)
        exec(split["code"], variables)
        if split["export"]:
            __VeRyYyY_sPecIAl_vars = make_special(variables)
            diff = get_dict_diff(__VeRyYyY_sPecIAl_vars, __VeRyYyY_sPecIAl_temp)
            diffs.update(diff)
    return diffs


# Utils

def make_special(a_dict: dict) -> dict:
    special_dict = {
        key: value for key, value in a_dict.items()
        if (key not in EXCEPTION_KEYS) and not key.startswith("__VeRyYyY_sPecIAl_")
    }
    return special_dict


def get_dict_diff(a_dict: dict, b_dict: dict) -> dict:
    diff = {}
    for key, value in a_dict.items():
        if key not in b_dict.keys():
            diff[key] = value
            continue
        if value != b_dict[key]:
            diff[key] = value
            continue
    return diff
