from typing import Union
import logging

from boar.__init__ import BoarError


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
