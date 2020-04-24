import json


def run_notebook(notebook_path: str) -> None:
    """Run notebook one cell and one line at a time.

    Parameters
    ----------
    notebook_path : str
        Path of notebook
    """
    with open(notebook_path, "r") as content_file:
        content = content_file.read()
    notebook_json = json.loads(content)
    cells = [cell["source"] for cell in notebook_json["cells"] if cell["cell_type"] == "code"]

    for cell_index, cell in enumerate(cells):
        lines = [line.replace("plt.show()", "plt.draw(); plt.close('all')") for line in cell]
        sources = [line for line in lines if not (line.startswith("%") or line.startswith("!"))]
        compact_source = "\n".join(sources)
        print(50*"-")
        print(f"Cell {cell_index}")
        print(50*"-")
        print(compact_source)
        print("\n")
        exec(compact_source)

    try:
        exec("plt.close('all')")
    except NameError:
        print("Notebook does not use matplotlib")
        pass
    return
