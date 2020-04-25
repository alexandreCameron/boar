from pathlib import Path

init_path = Path(__file__)
LIB_PATH = init_path.parents[0]
ROOT_PATH = init_path.parents[2]
NOTEBOOK_PATH = Path(ROOT_PATH, "notebook")
NOTEBOOK_PATH_00 = Path(NOTEBOOK_PATH, "00-test")
TESTS_PATH = Path(ROOT_PATH, "tests")
