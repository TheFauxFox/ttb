from pathlib import Path


def run(script_name: str) -> None:
    BASE: Path = Path(__file__).parent.parent.resolve() / "mods"
    script: Path = Path(BASE / f"{script_name}.py")
    if script.exists():
        script.unlink()


help: str = "Deletes a script"
aliases = ("delete", "rm")
usage: str = "del <command_name>"
