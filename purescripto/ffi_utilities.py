import git
from purescripto.configure_consts import *
from distutils.dir_util import remove_tree
from urllib.parse import urlsplit


def auto_link_repo(git_url: str, update=False) -> git.Repo:
    # Got a case insensitive name which can be used as
    # path in all platform, and has a bidirectional mapping
    # between the original url.
    spt = urlsplit(git_url)
    if not spt.path:
        raise ValueError("invalid git repo: {}".format(git_url))
    dir = PSPY_HOME / "repos" / spt.netloc
    dir.mkdir(parents=True, exist_ok=True)
    repo_path = dir.joinpath(spt.path[1:])

    if not repo_path.exists():
        repo = git.Repo.clone_from(git_url, str(repo_path))
    elif not (repo_path / ".git").exists():
        remove_tree(str(repo_path))
        repo = git.Repo.clone_from(git_url, str(repo_path))
    else:
        repo = git.Repo(str(repo_path))

    if update:
        # noinspection PyUnboundLocalVariable
        repo.git.pull('origin')

    return repo
