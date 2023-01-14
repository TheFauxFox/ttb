from pathlib import Path

from git import FetchInfo, Repo

from .fancy_print import rprint


def get_repo_name_from_url(url: str) -> str:
    # https://stackoverflow.com/a/55137835
    last_slash_index: int = url.rfind("/")
    last_suffix_index: int = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1 : last_suffix_index]  # noqa: 203


def clone_repo(url: str) -> Path:
    repo_name: str = get_repo_name_from_url(url)
    repo_dir: Path = (
        Path(__file__).parent.parent.resolve() / f"repos/{repo_name}"
    )
    if repo_dir.exists():
        fetch_info: list[FetchInfo] = Repo(repo_dir).remote().pull()
        if fetch_info[0].flags == 64:
            rprint(f'Updated repo "{repo_name}"')
    else:
        Repo.clone_from(
            url,
            repo_dir,
        )
        rprint(f'Cloning repo "{repo_name}"')
    return repo_dir
