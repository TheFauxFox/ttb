from pathlib import Path


def get_path(insensitive_path: Path | str) -> Path:
    rpath: Path = Path(insensitive_path).resolve()
    if rpath.exists():
        return rpath
    path: Path = Path(rpath.root)
    for part in rpath.parts:
        temp_path: Path = Path(path / part)
        if temp_path.exists():
            path = temp_path
        else:
            matches: list[Path] = [
                z
                for z in path.iterdir()
                if z.parts[-1].lower() == part.lower()
            ]
            if matches:
                path = Path(path / matches[0].parts[-1])
    return path
