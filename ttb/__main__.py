#!/usr/bin/env python3
import glob
from pathlib import Path
from types import ModuleType
from typing import Dict

from utils.history_console import HistoryConsole
from utils.import_file import import_file

TTB_DIR: str = str(Path(__file__).parent.resolve())
MOD_DIR: Path = Path(f"{TTB_DIR}/mods/")
BUILTIN_DIR: Path = Path(f"{TTB_DIR}/builtins/")

mod_files: list[str] = glob.glob(f"{MOD_DIR}/*.py")
builtin_files: list[str] = glob.glob(f"{BUILTIN_DIR}/*.py")

mods: Dict[str, ModuleType] = {}
mod_aliases: Dict[str, str] = {}
modfiles = [
    *[(MOD_DIR, x) for x in mod_files],
    *[(BUILTIN_DIR, x) for x in builtin_files],
]
for path, mod in modfiles:
    mod_path: Path = path / mod
    imported_mod: ModuleType | None = import_file(mod_path)
    if imported_mod is not None:
        if hasattr(imported_mod, "aliases"):
            for item in imported_mod.aliases:
                mod_aliases[item] = mod_path.stem
        mods[mod_path.stem] = imported_mod

mod_names: set[str] = set(mods.keys())
alias_names: set[str] = set(mod_aliases.keys())

inp: HistoryConsole = HistoryConsole("ttb", f"{TTB_DIR}/.hist")

while True:
    try:
        mod_cmd: str = str(
            inp.raw_input(
                "[bold][magenta]ttb[/magenta][/bold] [bold][bright_white]>"
            )
        )
        if len(mod_cmd) > 0:
            cmd, *args = mod_cmd.split()
            if cmd == "cmds":
                print(list(mod_names))
            elif cmd in mod_names:
                if args:
                    mods[cmd].run(*args)
                else:
                    mods[cmd].run()
            elif cmd in alias_names:
                if args:
                    mods[mod_aliases[cmd]].run(*args)
                else:
                    mods[mod_aliases[cmd]].run()
            else:
                print("Unknown command (> cmds) for list of commands")
    except (KeyboardInterrupt, EOFError):
        print("\n^Exit")
        break
