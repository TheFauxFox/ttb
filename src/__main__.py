#!/usr/bin/env python3
from glob import glob
import json
from pathlib import Path
import readline
from shlex import split
import sys
from types import ModuleType

from rich.table import Table
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .utils.fancy_print import rprint
from .utils.get_args import get_arg_len
from .utils.history_console import HistoryConsole
from .utils.import_file import import_file

TTB_DIR: str = str(Path(__file__).parent.resolve())
MOD_DIR: Path = Path(f"{TTB_DIR}/mods/")
BUILTIN_DIR: Path = Path(f"{TTB_DIR}/builtins/")
CONFIG: dict[str, str] = json.load(
    Path(Path(TTB_DIR).parent / "config.json").open("r")
)

mods: dict[str, ModuleType] = {}
mod_aliases: dict[str, str] = {}


def load_modules() -> None:
    global mods, mod_aliases
    mod_files: list[str] = glob(f"{MOD_DIR}/*.py")
    builtin_files: list[str] = glob(f"{BUILTIN_DIR}/*.py")
    mods = {}
    mod_aliases = {}
    modfiles: list[tuple[Path, str]] = [
        *[(MOD_DIR, x) for x in mod_files if not x.lower().endswith("__.py")],
        *[
            (BUILTIN_DIR, x)
            for x in builtin_files
            if not x.lower().endswith("__.py")
        ],
    ]
    for path, mod in modfiles:
        mod_path: Path = path / mod
        imported_mod: ModuleType | None = import_file(mod_path)
        if imported_mod is not None:
            if hasattr(imported_mod, "aliases"):
                for item in imported_mod.aliases:
                    mod_aliases[item] = mod_path.stem
            mods[mod_path.stem] = imported_mod


load_modules()
mod_names: set[str] = set(mods.keys())
alias_names: set[str] = set(mod_aliases.keys())


def reload() -> None:
    global mod_names, alias_names
    load_modules()
    mod_names = set(mods.keys())
    alias_names = set(mod_aliases.keys())


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(_):  # type: ignore
        reload()

    @staticmethod
    def on_created(_):  # type: ignore
        reload()


def custom_completion(text: str, state: int) -> str | None:
    options: list[str] = [
        x for x in [*mod_names, *alias_names] if x.startswith(text)
    ]
    try:
        return options[state]
    except IndexError:
        return None


readline.set_completer(custom_completion)

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


evt_handler = Handler()
observer = Observer()
observer.schedule(evt_handler, path=MOD_DIR, recursive=True)
observer.schedule(evt_handler, path=BUILTIN_DIR, recursive=True)
observer.start()

while True:
    try:
        mod_cmd: str = str(inp.raw_input(CONFIG["prompt"]))
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
                rprint("Unknown command `cmds` for list of commands")
    except (KeyboardInterrupt, EOFError):
        print("\n^Exit")
        observer.stop()
        break

observer.join()
sys.exit(0)
