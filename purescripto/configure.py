"""
The configuration file .pure-py.json has following keys, whose values are all strings.
- spago: the path of spago command, default: "spago".
- index-mirror: the name of python FFI mirror used, default: "default".
- blueprint: the path of `pspy-blueprint`, default: `pspy-blueprint`
- python-package: the name of output python package,
                  default to be the name of current directory,
                  with dashs replaced by underscores.
- corefn-dir: the name of corefn directory, default to be "output"

You'd better add following paths to .gitignore :
- pure-py.json
- .pure-py/
"""
from importlib import import_module
from typing import Dict, List, Iterable
from subprocess import check_call
from distutils.dir_util import copy_tree
from purescripto.configure_consts import *
from purescripto.utilities import auto_link_repo, import_from_path
import json
import sys
import os
import wisepy2

_TEMPLATE = {
    CKey.CoreFnDir  : CValue.CoreFnDir,
    CKey.EntryModule: CValue.EntryModule,
    CKey.BluePrint  : CValue.BluePrint,
    CKey.IndexMirror: CValue.IndexMirror,
    CKey.DataFormat : CValue.DataFormat,
}


def warn(s: str):
    print(wisepy2.Yellow(s))


def mk_ps_blueprint_cmd(
    pspy_blueprint,
    python_pack_name: str,
    entry: str,
    ffi_deps_path: str,
    format: str,
):
    return [
        pspy_blueprint,
        "--py-dir",
        python_pack_name,
        "--entry-mod",
        entry,
        "--ffi-dep",
        ffi_deps_path,
        "--out-format",
        format,
    ]


def solve_ffi(conf: CValue, update_mirror: bool) -> Iterable[str]:
    mirror_name = conf.IndexMirror
    mirror_repo = PSPY_HOME / "mirrors" / mirror_name

    if update_mirror:
        import git

        if not mirror_repo.exists():
            warn("The mirror {} not found at {}".format(mirror_name, str(mirror_repo)))
            if mirror_name == "default":
                warn(
                    "We're going to clone the mirror"
                    "https://github.com/purescript-python/purescript-python-ffi-index,\n"
                    "to ~/.pspy/mirrors/default."
                )
                git.Repo.clone_from(
                    r"https://github.com/purescript-python/purescript-python-ffi-index",
                    str(mirror_repo),
                )
            else:
                raise IOError("Mirror not found")
        git.Repo(str(mirror_repo)).git.pull("origin")

    mirror_entry = mirror_repo / "entry.py"

    if not mirror_entry.exists():
        if mirror_name != "default":
            raise IOError(
                "Mirror {} not found in {}".format(mirror_name, mirror_entry.parent)
            )
        else:
            import git

            warn("The mirror {} not found at {}".format(mirror_name, str(mirror_repo)))
            if mirror_name == "default":
                warn(
                    "We're going to clone the mirror"
                    "https://github.com/purescript-python/purescript-python-ffi-index,\n"
                    "to ~/.pspy/mirrors/default."
                )
                git.Repo.clone_from(
                    r"https://github.com/purescript-python/purescript-python-ffi-index",
                    str(mirror_repo),
                )

    mirror_mod = import_from_path(mirror_name, str(mirror_entry))
    solve_github_repo_url = mirror_mod.solve

    pspy_local_path = Path(STR_PY_PSC_LOCAL_PATH)
    ffi_deps = pspy_local_path / STR_FFI_DEPS_FILENAME
    with ffi_deps.open() as f:
        deps = f.read().splitlines()

    cache = set()  # to avoid returning duplicated repo

    for dep in deps:
        parts = Path(dep).parts
        if len(parts) > 3 and parts[0] == ".spago":
            _, package_name, version_, *_ = parts

            # assure unique
            cache_key = (package_name, version_)
            if cache_key in cache:
                continue
            cache.add(cache_key)

            version = [int(each) for each in version_[1:].split(".")]  # type: List[int]

            # return a string, available at current machine
            yield solve_github_repo_url(package_name, version)


FILES_TO_IGNORE = ['.pure-py/']
def pspy(
    run: bool = False, version: bool = False, init: bool = False, update: bool = False
):
    """PureScript Python compiler
    --run     : running without rebuild(note that `spago run` will rebuild the code)
    --version : version of your purescript-python wrapper(purescripto)
    --init    : setup purescript-python components for a spago project
    --update  : sync with latest mirror and Python FFI dependencies

example use:
    Create a pspy project:
        sh> mkdir purescript-xxx && cd purescript-xxx && spago init && pspy --init
    Update project's dependencies:
        sh> cd purescript-xxx && pspy --update
    Build your project:
        sh> pspy
    """
    path = Path().absolute()
    pure_py_conf = path / "pure-py.json"
    py_pack_name_default = path.name.replace("-", "_")
    if init:
        if not pure_py_conf.exists():
            with pure_py_conf.open("w") as f:
                json.dump(_TEMPLATE, f, indent=2, sort_keys=True)

            ignore_file = path / ".gitignore"
            with ignore_file.open("a+") as f:
                is_configured = {k: True for k in FILES_TO_IGNORE}
                for each in f.readlines():
                    if each in FILES_TO_IGNORE:
                        is_configured[each] = False

                xs = [k for k, v in is_configured.items() if v]
                if xs:
                    f.write("\n# purescript-python\n")
                    for x in xs:
                        f.write(x)
                        f.write("\n")

            local_dir = path / STR_PY_PSC_LOCAL_PATH
            local_dir.mkdir(parents=True, exist_ok=True)
            (local_dir / STR_FFI_DEPS_FILENAME).open("w").close()
        return

    # init conf
    if pure_py_conf.exists():
        with pure_py_conf.open() as f:
            conf_dict = json.load(f)  # type: Dict[str, str]
    else:
        conf_dict = {}

    conf_dict.setdefault(CKey.IndexMirror, CValue.IndexMirror)
    conf_dict.setdefault(CKey.BluePrint, CValue.BluePrint)
    conf_dict.setdefault(CKey.PyPack, py_pack_name_default)
    conf_dict.setdefault(CKey.CoreFnDir, CValue.CoreFnDir)
    conf_dict.setdefault(CKey.EntryModule, CValue.EntryModule)
    conf_dict.setdefault(CKey.DataFormat, CValue.DataFormat)

    conf = CValue()
    conf.IndexMirror = conf_dict[CKey.IndexMirror]
    conf.BluePrint = conf_dict[CKey.BluePrint]
    conf.PyPack = conf_dict[CKey.PyPack]
    conf.CoreFnDir = conf_dict[CKey.CoreFnDir]
    conf.EntryModule = conf_dict[CKey.EntryModule]
    conf.DataFormat = conf_dict[CKey.DataFormat]

    # TODO: currently unused.
    #   support custom corefn output path in pspy-blueprint.
    corefn_dir = path / conf.CoreFnDir

    # run commands
    if run:
        sys.path.append(str(path))
        mod = import_module("{}.{}.pure".format(conf.PyPack, conf.EntryModule))
        if hasattr(mod, "main"):
            mod.main()
        return
    elif version:
        from purescripto.version import __version__

        print("{}".format(__version__))
        return

    pspy_local_path = Path(STR_PY_PSC_LOCAL_PATH)

    if not pspy_local_path.exists():
        pspy_local_path.mkdir(parents=True)

    ffi_deps_file = pspy_local_path / STR_FFI_DEPS_FILENAME
    cmd = mk_ps_blueprint_cmd(
        conf.BluePrint,
        conf.PyPack,
        conf.EntryModule,
        str(ffi_deps_file),
        conf.DataFormat,
    )
    try:
        check_call(cmd)
    except FileNotFoundError:
        print(
            "It seems that your pspy-blueprint command hasn't got installed\n"
            r"Go to this page: https://github.com/purescript-python/purescript-python/releases,"
            "\n"
            r"download exe for your platform, and add it to your PATH."
        )
        sys.exit(1)

    path_join = os.path.join
    python_ffi_path = Path(conf.PyPack) / "ffi"
    if not python_ffi_path.exists():
        python_ffi_path.mkdir(parents=True)
    python_ffi_path = str(python_ffi_path)

    # copy python ffi files
    for repo_url in solve_ffi(conf, update_mirror=update):
        repo = auto_link_repo(repo_url, update=update)
        copy_tree(path_join(repo.working_dir, "python-ffi"), python_ffi_path)

    python_ffi_provided_by_current_proj = path / "python-ffi"
    if python_ffi_provided_by_current_proj.exists():
        copy_tree(str(python_ffi_provided_by_current_proj), python_ffi_path)

    # fill __init__.py
    for dir, _, files in os.walk(conf.PyPack):
        if "__init__.py" not in files:
            open(path_join(dir, "__init__.py"), "w").close()
