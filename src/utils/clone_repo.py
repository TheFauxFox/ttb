from pathlib import Path

from git import FetchInfo, Repo

from .fancy_print import rprint
from .giturlparse import parse, Parsed


def clone_repo(url: str) -> Path:
    repo_info: Parsed = parse(url)
    repo_name: str = repo_info.name
    repo_owner: str = repo_info.owner
    repo_dir: Path = (
        Path(__file__).parent.parent.resolve() / f"repos/{repo_name}"
    )
    if repo_dir.exists():
        fetch_info: list[FetchInfo] = Repo(repo_dir).remote().pull()
        if fetch_info[0].flags == 64:
            rprint(f'Updated repo "{repo_owner}/{repo_name}"')
    else:
        Repo.clone_from(
            url,
            repo_dir,
        )
        rprint(f'Cloning repo "{repo_owner}/{repo_name}"')
    return repo_dir
