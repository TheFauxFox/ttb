import atexit
import code
from contextlib import suppress
from pathlib import Path
import readline

from .fancy_print import rprint


class HistoryConsole(code.InteractiveConsole):
    def __init__(
        self,
        filename: str,
        histfile: str | Path,
    ) -> None:
        code.InteractiveConsole.__init__(self, None, filename)
        self.init_history(histfile)

    def init_history(self, histfile: str | Path) -> None:
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            with suppress(FileNotFoundError):
                readline.read_history_file(histfile)
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile: str | Path) -> None:
        readline.set_history_length(1000)
        readline.write_history_file(histfile)

    def raw_input(self, prompt: str = ">") -> str:
        rprint(prompt, end="")
        return input(" ")
