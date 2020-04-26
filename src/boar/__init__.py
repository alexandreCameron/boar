from pathlib import Path

# Paths
init_path = Path(__file__)
LIB_PATH = init_path.parents[0]
ROOT_PATH = init_path.parents[2]
NOTEBOOK_PATH = Path(ROOT_PATH, "notebook")
NOTEBOOK_PATH_00 = Path(NOTEBOOK_PATH, "00-test")
NOTEBOOK_PATH_01 = Path(NOTEBOOK_PATH, "01-io")
TESTS_PATH = Path(ROOT_PATH, "tests")

# Tags
START_TAG = "boar_export_start"
END_TAG = "boar_export_end"
SELECT_TAG = "boar_export_select"


class BoarError(Exception):
    pass
