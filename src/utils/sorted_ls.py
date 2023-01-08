import os
from typing import List, Tuple


def sorted_ls(path: str) -> List[Tuple[str, float]]:
    def mtime(entry: os.DirEntry[str]) -> float:
        return entry.stat().st_mtime

    return sorted(
        ((entry.name, mtime(entry)) for entry in os.scandir(path)),
        key=lambda x: x[1],
        reverse=True,
    )
