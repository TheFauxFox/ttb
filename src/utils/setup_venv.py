from pathlib import Path
import venv


def get_venv() -> Path:
    VENV_PATH: Path = Path(__file__).parent.parent.resolve() / ".venv"

    if not VENV_PATH.exists():
        venv.create(
            VENV_PATH,
            symlinks=True,
            with_pip=True,
        )
    return VENV_PATH


# This is a really really dumb thing to do, however there's a decent reason.
# Implementing alternative mod dirs and adding potential repo support, there
# 100% will be reason to need a secondary requirements.txt file. Personally,
# I have an issue forcefully installing to a user's packages. This will
# (hopefully) work as a dummy way to have a venv to hold all those packages.
