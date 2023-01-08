from pathlib import Path

import editor  # types: ignore


def run(script_name: str) -> None:
    default = (
        'def run() -> None:\n    pass\n\nhelp: str = ""'
        + f'\nusage: str = "{script_name}"\naliases = ()\n'
    )
    BASE: Path = Path(__file__).parent.parent.resolve() / "mods"
    script: Path = Path(BASE / f"{script_name}.py")
    scriptstr: str = str(script)
    if script.exists():
        editor(filename=scriptstr)
    else:
        editor(filename=scriptstr, text=default)


help: str = "Creates a new command or edits a previous one"
aliases = ("edit",)
usage: str = "new <command_name>"
