from typing import List, Tuple, Any
import logging

from boar.__init__ import BoarError


def log_execution(
    cell_index: int,
    msg: str,
    verbose: Any,
) -> None:
    logger_print = get_logger_print(verbose)
    logger_print(50*"-")
    logger_print(f"Cell {cell_index}")
    logger_print(50*"-")
    logger_print(msg)
    logger_print("\n")


def log_lint(
    file_posix: str,
    cell_counts: List[Tuple[int]],
    verbose: Any,
) -> None:
    logger_print = get_logger_print(verbose)
    logger_print(50*"-")
    logger_print(file_posix)
    logger_print(50*"-")
    for cell_count in cell_counts:
        msg = f"Cell: {cell_count[0]} , execution_count: {cell_count[1]}"
        logger_print(msg)
    logger_print("\n")


def get_logger_print(verbose: Any):
    logger_print = (lambda x: None)
    if isinstance(verbose, bool):
        logger_print = print if verbose else logging.info
    elif isinstance(verbose, object):
        logger_print = verbose
    else:
        msg = f"Undefined verbose: `{verbose}`."
        raise BoarError(msg)
    return logger_print


def close_plots():
    try:
        exec("plt.close('all')")
    except NameError:
        logging.debug("Notebook does not use matplotlib")
        pass
