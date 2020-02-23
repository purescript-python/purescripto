import git
from purescripto.configure_consts import *
from distutils.dir_util import remove_tree
from urllib.parse import urlsplit
from importlib.util import spec_from_file_location, module_from_spec


def import_from_path(name, path):
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def auto_link_repo(git_url: str, update: bool) -> git.Repo:
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
        print('Initializing repo {} to local storage..'.format(git_url))
        repo = git.Repo.clone_from(git_url, str(repo_path))
    elif not (repo_path / ".git").exists():
        print('Git repo {}\'s local storage missed .git, fixing..'.format(
            git_url, repo_path))
        remove_tree(str(repo_path))
        repo = git.Repo.clone_from(git_url, str(repo_path))
    else:
        repo = git.Repo(str(repo_path))

    if update:
        # noinspection PyUnboundLocalVariable
        print('Updateing {}..'.format(repo))
        repo.git.pull('origin')
        print('Git repo updated!')

    return repo
