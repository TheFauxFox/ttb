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

from .utils.clone_repo import clone_repo
from .utils.fancy_print import print_error, rprint
from .utils.get_args import get_arg_len
from .utils.history_console import HistoryConsole
from .utils.import_file import import_file

TTB_DIR: str = str(Path(__file__).parent.resolve())
MOD_DIR: Path = Path(f"{TTB_DIR}/mods/")
BUILTIN_DIR: Path = Path(f"{TTB_DIR}/builtins/")
CONFIG: dict[str, str] = json.load(
    Path(Path(TTB_DIR).parent / "config.json").open("r")
)


def is_valid_mod_dir(path: Path) -> Path | None:
    if not path.exists():
        print_error(f"Could not resolve '{path.resolve()}'")
        return None
    if (path / "mods").exists():
        return path
    elif path.stem == "mods":
        return path.parent
    else:
        print_error(f"'{path.resolve()}' is not a valid module directory")
        return None


def get_local_mod_dirs() -> set[Path]:
    out: set[Path] = set()
    for path in [Path(p) for p in CONFIG["local_dirs"]]:
        valid: Path | None = is_valid_mod_dir(path)
        if valid:
            out.add(valid)
    return out


def get_valid_repos() -> set[Path]:
    out: set[Path] = set()
    repos: set[Path] = set()
    for repo in CONFIG["repositories"]:
        REPO_DIRS.add(clone_repo(repo))
    for path in repos:
        valid: Path | None = is_valid_mod_dir(path)
        if valid:
            out.add(valid)
    return out


CUSTOM_DIRS: set[Path] = get_local_mod_dirs()
REPO_DIRS: set[Path] = get_valid_repos()

mods: dict[str, ModuleType] = {}
mod_aliases: dict[str, str] = {}


def load_modules() -> None:
    global mods, mod_aliases
    mod_files: list[str] = glob(f"{MOD_DIR}/*.py")
    builtin_files: list[str] = glob(f"{BUILTIN_DIR}/*.py")
    repo_files: list[tuple[Path, str]] = []
    custom_files: list[tuple[Path, str]] = []

    for repo_path in REPO_DIRS:
        repo_files.extend(
            [
                (Path(f"{repo_path}/mods"), f)
                for f in glob(f"{repo_path}/mods/*.py")
            ]
        )

    for custom_path in CUSTOM_DIRS:
        custom_files.extend(
            [
                (Path(f"{custom_path}/mods"), f)
                for f in glob(f"{custom_path}/mods/*.py")
            ]
        )

    mods = {}
    mod_aliases = {}

    def is_valid(fn: str) -> bool:
        return not fn.lower().endswith("__.py")

    modfiles: list[tuple[Path, str]] = [
        *[(BUILTIN_DIR, fn) for fn in builtin_files if is_valid(fn)],
        *[(MOD_DIR, fn) for fn in mod_files if is_valid(fn)],
        *[(path, fn) for path, fn in custom_files if is_valid(fn)],
        *[(path, fn) for path, fn in repo_files if is_valid(fn)],
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
for path in [*REPO_DIRS, *CUSTOM_DIRS]:
    observer.schedule(evt_handler, path=path, recursive=True)
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
