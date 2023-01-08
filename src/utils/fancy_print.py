from rich.console import Console

console = Console(color_system="truecolor")
rprint = console.print
jprint = console.print_json
cinput = console.input


def get_style_codes(txt):
    with console.capture() as capture:
        rprint(txt, end=" ")
    return capture.get()
