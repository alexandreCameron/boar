from pathlib import Path
from enum import Enum

# Paths
init_path = Path(__file__)
LIB_PATH = init_path.parents[0]
ROOT_PATH = init_path.parents[2]
TESTS_PATH = Path(ROOT_PATH, "tests")


# Tags

class Tag(Enum):
    EXPORT = "# export_"
    EXPORT_START = f"{EXPORT}start"
    EXPORT_END = f"{EXPORT}end"
    EXPORT_LINE = f"{EXPORT}line"
    SKIP = "# skip_"
    SKIP_START = f"{SKIP}start"
    SKIP_END = f"{SKIP}end"
    SKIP_LINE = f"{SKIP}line"


class Notebook(Enum):
    MAIN = Path(ROOT_PATH, "notebook")
    _00 = Path(MAIN, "00-test")
    _01 = Path(MAIN, "01-io")
    _02 = Path(MAIN, "02-lint")


class ErrorLabel(Enum):
    LINT = "Linting"
    ASSERT = "Assertion"
    RUN = "Execution"


class BoarError(Exception):
    pass


def get_raw_exec():
    raw_exec = {}
    exec("", raw_exec)
    return raw_exec


EXCEPTION_KEYS = list(get_raw_exec().keys())
