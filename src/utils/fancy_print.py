from rich.console import Console

console = Console(color_system="truecolor")
rprint = console.print
jprint = console.print_json
cinput = console.input


def print_error(txt: str) -> None:
    rprint(f"[[red]ERR[/red]]: {txt}")


def get_style_codes(txt: str) -> str:
    with console.capture() as capture:
        rprint(txt, end="")
    return capture.get()
