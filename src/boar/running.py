from pathlib import Path
from enum import EnumMeta

from typing import Union

from boar.__init__ import Tag, BoarError, VERBOSE
from boar.utils.log import (log_execution, close_plots)
from boar.utils.parse import (get_code_sources, strap_source_in_one_line, check_is_notebook)
from boar.utils.execute import (execute_by_block, execute_by_line)
from copy import deepcopy


def run_notebook(
    notebook_path: Union[str, Path],
    inputs: dict = {},
    verbose: Union[bool, object] = VERBOSE,
    Tag: EnumMeta = Tag,
) -> dict:
    """Run notebook one cell and one line at a time.

    Parameters
    ----------
    notebook_path : Union[str, Path]
        Path of notebook
    inputs : dict, optional
        Parameter to set before launching the script, by default {}
    verbose: Union[bool, object], optional
        Option to print more information, by default False
    Tag : EnumMeta, optional
        Name of the tags, by default Tag

    Returns
    -------
    dict
        Outputs to return if `export`-tags set in notebook

    Raises
    ------
    BoarError
        If `export*` and `skip*` tags in the same source
    BoarError
        If `*start` and `*line` tags in the same source
    """
    # Parse json
    notebook_path = check_is_notebook(notebook_path)
    sources = get_code_sources(notebook_path)

    # Run set new inputs
    locals().update(inputs)

    # Run Code
    outputs = {}
    for cell_index, source in enumerate(sources):
        # Parse source lines for execution
        source_to_exec = strap_source_in_one_line(source)
        log_execution(cell_index, source_to_exec, verbose=verbose)

        # Run, if no export tag
        if (Tag.EXPORT.value not in source_to_exec) and (Tag.SKIP.value not in source_to_exec):
            exec(source_to_exec)
            continue

        # Raise error if too different tag type
        if (Tag.EXPORT.value in source_to_exec) and (Tag.SKIP.value in source_to_exec):
            msg = f"`{Tag.EXPORT.value}*` and `{Tag.EXPORT.value}*` cannot be in same cell."
            raise BoarError(msg)

        # Define tags
        if (Tag.EXPORT.value in source_to_exec):
            start_tag = Tag.EXPORT_START.value
            end_tag = Tag.EXPORT_END.value
            line_tag = Tag.EXPORT_LINE.value

        if (Tag.SKIP.value in source_to_exec):
            start_tag = Tag.SKIP_START.value
            end_tag = Tag.SKIP_END.value
            line_tag = Tag.SKIP_LINE.value

        # Raise error if incompatible extensions
        if (start_tag in source_to_exec) and (line_tag in source_to_exec):
            msg = f"`{start_tag}` and `{line_tag}` cannot be in same cell."
            raise BoarError(msg)

        # Executre python code
        if start_tag in source_to_exec:
            diffs = execute_by_block(source_to_exec, start_tag, end_tag, locals())
            outputs.update(diffs)
            continue

        if line_tag in source_to_exec:
            diffs = execute_by_line(source_to_exec, line_tag, locals())
            outputs.update(diffs)
            continue

    close_plots()
    return deepcopy(outputs)
