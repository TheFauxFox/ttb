from pathlib import Path
import subprocess

from setup_venv import get_venv


def install(package: str) -> None:
    exe: Path = get_venv() / "bin/python"
    subprocess.check_call(
        [str(exe.resolve()), "-m", "pip", "install", package]
    )
