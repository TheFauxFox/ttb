import json
from pathlib import Path

from src.utils.clone_repo import clone_repo
from src.utils.giturlparse import parse


def run(repo_name: str | None = None) -> None:
    CONFIG: dict[str, str] = json.load(
        Path(Path(__file__).parent.parent.parent / "config.json").open("r")
    )
    for repo in CONFIG["repositories"]:
        if repo_name is not None and parse(repo).name != repo_name:
            continue
        clone_repo(repo)


help: str = (
    "Pulls all listed repositories or a single specified repo "
    + "that's listed in the config"
)
usage: str = "refresh [repo_name]"
aliases = ("r",)
