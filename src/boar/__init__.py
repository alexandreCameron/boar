from pathlib import Path
from enum import Enum

# Paths
init_path = Path(__file__)
LIB_PATH = init_path.parents[0]
ROOT_PATH = init_path.parents[2]
TESTS_PATH = Path(ROOT_PATH, "tests")


# Tags

class Tag(Enum):
    EXPORT_START = "export_start"
    EXPORT_END = "export_end"
    EXPORT_LINE = "export_line"
    SKIP_LINE = "skip_line"


class Notebook(Enum):
    MAIN = Path(ROOT_PATH, "notebook")
    _00 = Path(MAIN, "00-test")
    _01 = Path(MAIN, "01-io")


class BoarError(Exception):
    pass


def get_raw_exec():
    raw_exec = {}
    exec("", raw_exec)
    return raw_exec


EXCEPTION_KEYS = list(get_raw_exec().keys())
