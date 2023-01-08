# ttb
### TerminalToolBox
Listen. I'm lazy as hell, and would rather spend my time making half-assed scripts to make my life
barely more efficient. I know I could spend the time it takes to make a script doing what I'm supposed
to, but that's just no fun. So why not make a janky and entirely unnecessary yet still enjoyable
project based around a box of random scripts that I might only use once?


## Usage

First off, fork the repo. I don't care to have *your* scripts in *my* toolbox.

Besides that, throw some random scripts into the `mods` directory and presto, whatever the name
of the file is, is the name of the command!

There's a bit of a layout for it though, and there's probably plenty to optimize.

The basic script layout is this:


```python
# command.py
help = "Some description, help string, or argument list. Whatever you decide." # Optional. Will be left blank if it doesn't exist
usage = "command <message> [optional_param]" # Optional. Will be left blank if it doesn't exist. Good idea to have though.
aliases = ("cmd", "c", "some_random_alias") # Optional. If left empty, it can only be run from the name of the file.

def run(*args): # Required. *args should be replaced with actual argument names
    print(args) # Placeholder, do something with it I guess
```
It's a good idea to __*not*__ use spaces in the file name or aliases, as all arguments are currently split on spaces.
Have fun with that!

## TODO:
- [X] Implement `shlex` to allow for quoted arguments (aka allow for spaces lol)
- [X] Have some kind of hot-reload for quickly testing scripts without having to bail `ttb`
- [ ] Idk, make things pretty?