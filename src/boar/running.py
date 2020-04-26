import json
from pathlib import Path

from typing import List, Union

import logging
from boar.__init__ import START_TAG, END_TAG, SELECT_TAG, BoarError


def run_notebook(
    notebook_path: Union[str, Path],
    verbose: Union[bool, object] = False,
    start_tag: str = START_TAG,
    end_tag: str = END_TAG,
    select_tag: str = SELECT_TAG,
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
            diffs = execute_by_select(compact_source, select_tag, locals())
            outputs.update(diffs)
            continue

        exec(compact_source)

    close_plots()
    return outputs


# Line execution

def execute_by_select(compact_source: str, select_tag: str, variables: dict) -> dict:
    splits = split_lines_with_select_tag(compact_source, select_tag)

    diffs = {}
    for split in splits:
        if split["export"]:
            temp = dict(variables)
        exec(split["code"], variables)
        if split["export"]:
            diff = {key: variables[key] for key in set(variables) - set(temp) if key != "temp"}
            diffs.update(diff)
    return diffs


def split_lines_with_select_tag(
    source_to_split: str,
    tag: str,
) -> List[str]:
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


# Parsing

def get_notebook_cells(notebook_path: Union[str, Path]) -> List[str]:
    with open(notebook_path, "r") as json_stream:
        content = json.load(json_stream)
    cells = [cell["source"] for cell in content["cells"] if cell["cell_type"] == "code"]
    return cells


def parse_lines(cell: List[str]) -> str:
    lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
    sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
    compact_source = "".join(sources)
    return compact_source


# Block execution

def execute_by_block(compact_source: str, start_tag: str, end_tag: str, variables: dict) -> dict:
    """Implicit update for locals() !!!! But this behavior is wanted"""
    start_split = split_lines_with_block_tag(compact_source, start_tag)
    end_split = split_lines_with_block_tag(start_split[1], end_tag)

    exec(start_split[0], variables)
    temp = dict(variables)
    exec(end_split[0], variables)
    diffs = {key: variables[key] for key in set(variables) - set(temp) if key != "temp"}
    exec(end_split[1], variables)

    return diffs


def split_lines_with_block_tag(
    source_to_split: str,
    tag: str,
) -> List[str]:
    splits, block = [], []
    for line in source_to_split.split("\n"):
        if tag in line:
            splits.append("\n".join(block))
            block = []
            continue
        block.append(line)
    splits.append("\n".join(block))

    if len(splits) > 2:
        msg = f"Multiple `{tag}` in:\n{source_to_split}"
        raise BoarError(msg)
    return splits


# Cosmetic

def log_execution(
    cell_index: int,
    compact_source: str,
    verbose: Union[bool, object],
) -> None:
    logger_print = (lambda x: None)
    if isinstance(verbose, bool):
        logger_print = print if verbose else logging.info
    elif isinstance(verbose, object):
        logger_print = verbose
    else:
        msg = f"Undefined verbose: `{verbose}`."
        raise BoarError(msg)

    logger_print(50*"-")
    logger_print(f"Cell {cell_index}")
    logger_print(50*"-")
    logger_print(compact_source)
    logger_print("\n")


def close_plots():
    try:
        exec("plt.close('all')")
    except NameError:
        logging.debug("Notebook does not use matplotlib")
        pass
