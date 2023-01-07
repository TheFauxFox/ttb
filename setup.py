from pathlib import Path
import venv

venv.create(Path("./.venv"), symlinks=True, with_pip=True)
