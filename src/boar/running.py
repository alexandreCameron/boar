from pathlib import Path
from enum import EnumMeta

from typing import Union

from boar.__init__ import Tag, BoarError
from boar.utils.log import (log_execution, close_plots)
from boar.utils.parse import (get_notebook_cells, parse_lines)
from boar.utils.execute import (execute_by_block, execute_by_line)
from copy import deepcopy


def run_notebook(
    notebook_path: Union[str, Path],
    inputs: dict = {},
    verbose: Union[bool, object] = False,
    Tag: EnumMeta = Tag,
) -> dict:
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
        if (Tag.EXPORT.value not in compact_source) and (Tag.SKIP.value not in compact_source):
            exec(compact_source)
            continue

        # Raise error if too different tag type
        if (Tag.EXPORT.value in compact_source) and (Tag.SKIP.value in compact_source):
            msg = f"`{Tag.EXPORT.value}*` and `{Tag.EXPORT.value}*` cannot be in same cell."
            raise BoarError(msg)

        # Define tags
        if (Tag.EXPORT.value in compact_source):
            start_tag = Tag.EXPORT_START.value
            end_tag = Tag.EXPORT_END.value
            line_tag = Tag.EXPORT_LINE.value

        if (Tag.SKIP.value in compact_source):
            start_tag = Tag.SKIP_START.value
            end_tag = Tag.SKIP_END.value
            line_tag = Tag.SKIP_LINE.value

        # Raise error if incompatible extensions
        if (start_tag in compact_source) and (line_tag in compact_source):
            msg = f"`{start_tag}` and `{line_tag}` cannot be in same cell."
            raise BoarError(msg)

        # Executre python code
        if start_tag in compact_source:
            diffs = execute_by_block(compact_source, start_tag, end_tag, locals())
            outputs.update(diffs)
            continue

        if line_tag in compact_source:
            diffs = execute_by_line(compact_source, line_tag, locals())
            outputs.update(diffs)
            continue

    close_plots()
    return deepcopy(outputs)
