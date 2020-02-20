import git
import base64
from pathlib import Path
from purescripto.configure_consts import *
from distutils.dir_util import remove_tree
_pspy_home = Path(PSPY_HOME)
if not _pspy_home.exists():
    _pspy_home.mkdir(parents=True)


def auto_link_repo(git_url: str, update=False):
    # Got a case insensitive name which can be used as
    # path in all platform, and has a bidirectional mapping
    # between the original url.
    repo_name = base64.b32encode(git_url.encode('utf8')).decode('ascii')
    repo_path = _pspy_home / 'repos' / repo_name

    if not repo_path.exists():
        repo = git.Repo.clone_from(git_url, str(repo_path))
    elif not (repo_path / "git").exists():
        remove_tree(str(repo_path))
        repo = git.Repo.clone_from(git_url, str(repo_path))
    else:
        repo = git.Repo(str(repo_path))

    if update:
        # noinspection PyUnboundLocalVariable
        repo.git.pull('origin')

    return repo
