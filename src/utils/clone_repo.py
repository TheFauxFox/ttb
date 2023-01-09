from pathlib import Path

from git import Repo


def get_repo_name_from_url(url: str) -> str:
    # https://stackoverflow.com/a/55137835
    last_slash_index: int = url.rfind("/")
    last_suffix_index: int = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1 : last_suffix_index]  # noqa: 203


def clone_repo(url: str) -> None:
    Repo.clone_from(
        url,
        Path(__file__).parent.resolve()
        / f"repos/{get_repo_name_from_url(url)}",
    )
