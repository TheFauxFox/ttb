import sys

aliases: tuple[str, ...] = (".exit", "q")
help: str = "Exits the program"


def run() -> None:
    sys.exit(0)
