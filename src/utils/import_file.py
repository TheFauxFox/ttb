from importlib.machinery import ModuleSpec
import importlib.util
from pathlib import Path
from types import ModuleType


def import_file(path: str | Path) -> ModuleType | None:
    file_path: Path = Path(path).resolve()
    module_name: str = file_path.stem

    spec: ModuleSpec | None = importlib.util.spec_from_file_location(
        module_name, file_path
    )
    if spec is not None and spec.loader is not None:
        module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None
