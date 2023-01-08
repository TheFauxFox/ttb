#!/usr/bin/env python3
import glob
from pathlib import Path
from shlex import split
from types import ModuleType

from rich.table import Table

from .utils.fancy_print import rprint
from .utils.get_args import get_arg_len
from .utils.history_console import HistoryConsole
from .utils.import_file import import_file

TTB_DIR: str = str(Path(__file__).parent.resolve())
MOD_DIR: Path = Path(f"{TTB_DIR}/mods/")
BUILTIN_DIR: Path = Path(f"{TTB_DIR}/builtins/")

mod_files: list[str] = glob.glob(f"{MOD_DIR}/*.py")
builtin_files: list[str] = glob.glob(f"{BUILTIN_DIR}/*.py")

mods: dict[str, ModuleType] = {}
mod_aliases: dict[str, str] = {}
modfiles: list[tuple[Path, str]] = [
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


def print_help(*module_names: str) -> None:
    table: Table = Table(
        "Command", "Aliases", "Usage", "Description", show_lines=True
    )
    for modname in module_names:
        mod: ModuleType = mods[modname]
        table.add_row(
            modname,
            ", ".join(mod.aliases) if hasattr(mod, "aliases") else "",
            mod.usage if hasattr(mod, "usage") else "",
            mod.help if hasattr(mod, "help") else "",
        )
    rprint(table)


while True:
    try:
        mod_cmd: str = str(
            inp.raw_input(
                "[bold][magenta]ttb[/magenta][/bold] [bold][bright_white]>"
            )
        )
        if len(mod_cmd.strip()) > 0:
            cmd, *args = split(mod_cmd)
            if cmd == "cmds":
                print_help(*mods.keys())
            elif cmd in mod_names:
                func = mods[cmd].run
                if args and get_arg_len(func) == len(args):
                    func(*args)
                elif get_arg_len(func) == 0:
                    func()
                else:
                    print_help(cmd)
            elif cmd in alias_names:
                func = mods[mod_aliases[cmd]].run
                if args and get_arg_len(func) == len(args):
                    func(*args)
                elif get_arg_len(func) == 0:
                    func()
                else:
                    print_help(cmd)
            else:
                print("Unknown command (> cmds) for list of command")
    except (KeyboardInterrupt, EOFError):
        print("\n^Exit")
        break
