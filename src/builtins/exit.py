import sys
from typing import Union

aliases: tuple[str, ...] = (".exit", "q")
help: str = "Exits the program"


def run(*args: Union[int, str]) -> None:
    sys.exit(0)
