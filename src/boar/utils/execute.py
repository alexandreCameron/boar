from typing import List, Dict, Union

from boar.utils.split import (split_lines_by_block, split_lines_with_line_tag)
from boar.__init__ import EXCEPTION_KEYS


def execute_by_block(compact_source: str, start_tag: str, end_tag: str, variables: dict) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    splits = split_lines_by_block(compact_source, start_tag, end_tag)
    return execute_python(splits, variables)


def execute_by_line(compact_source: str, line_tag: str, variables: dict) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    splits = split_lines_with_line_tag(compact_source, line_tag)
    return execute_python(splits, variables)


def execute_python(
    splits: List[Dict[str, Union[str, bool]]],
    variables: dict
) -> dict:
    """Implicit update of locals() !!!! But this behavior is wanted."""
    diffs = {}
    for split in splits:
        if (split["type"] == "skip") and split["apply"]:
            continue

        if (split["type"] == "export") and split["apply"]:
            __VeRyYyY_sPecIAl_temp = make_special(variables)
        exec(split["code"], variables)
        if (split["type"] == "export") and split["apply"]:
            __VeRyYyY_sPecIAl_vars = make_special(variables)
            diff = get_dict_diff(__VeRyYyY_sPecIAl_vars, __VeRyYyY_sPecIAl_temp)
            diffs.update(diff)
    return diffs


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
