from typing import List, Dict, Union

from boar.__init__ import BoarError


def split_lines_by_block(
    source_to_split: str,
    start_tag: str,
    end_tag: str,
) -> List[Dict[str, Union[str, bool]]]:
    print(source_to_split, start_tag, end_tag)
    tag_type = start_tag.split("# ")[1].split("_")[0]
    start_splits = split_lines_with_block_tag(source_to_split, start_tag)
    end_splits = split_lines_with_block_tag(start_splits[1], end_tag)

    splits = [
        {"code": start_splits[0], "type": tag_type, "apply": False},
        {"code": end_splits[0], "type": tag_type, "apply": True},
        {"code": end_splits[1], "type": tag_type, "apply": False},
    ]
    return splits


def split_lines_with_block_tag(
    source_to_split: str,
    tag: str,
) -> List[str]:
    block_splits, block = [], []
    for line in source_to_split.split("\n"):
        block.append(line)
        if tag in line:
            block_splits.append("\n".join(block))
            block = []
            continue
    block_splits.append("\n".join(block))

    if len(block_splits) > 2:
        msg = f"Multiple `{tag}` in:\n{source_to_split}"
        raise BoarError(msg)
    return block_splits


def split_lines_with_line_tag(
    source_to_split: str,
    tag: str,
) -> List[Dict[str, Union[str, bool]]]:
    tag_type = tag.split("_")[0].split("# ")[1]
    splits, block = [], []
    for line in source_to_split.split("\n"):
        if tag in line:
            splits.append({"code": "\n".join(block), "type": tag_type, "apply": False})
            splits.append({"code": line, "type": tag_type, "apply": True})
            block = []
            continue
        block.append(line)
    splits.append({"code": "\n".join(block), "type": tag_type, "apply": False})
    return splits
