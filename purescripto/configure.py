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
- .pure-py.json
- .pure-py/
"""
from importlib import import_module
from typing import Dict, List, Iterable
from subprocess import check_call
from importlib.util import spec_from_file_location, module_from_spec
from distutils.dir_util import copy_tree
from purescripto.configure_consts import *
from purescripto.ffi_utilities import auto_link_repo
import json
import sys
import os
import git

_TEMPLATE = {
    CKey.CoreFnDir: CValue.CoreFnDir,
    CKey.EntryModule: CValue.EntryModule,
    CKey.BluePrint: CValue.BluePrint,
    CKey.Spago: CValue.Spago,
    CKey.IndexMirror: CValue.IndexMirror
}


def mk_ps_blueprint_cmd(pspy_blueprint, python_pack_name: str, entry: str,
                        ffi_deps_path: str):
    return [
        pspy_blueprint,
        '--out-python',
        python_pack_name,
        '--corefn-entry',
        entry,
        '--out-ffi-dep',
        ffi_deps_path,
    ]


def import_from_path(name, path):
    spec = spec_from_file_location(name, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def solve_ffi(conf: CValue) -> Iterable[str]:
    mirror_name = conf.IndexMirror
    mirror_entry = PSPY_HOME / "mirrors" / mirror_name / "entry.py"
    if not mirror_entry.exists():
        raise IOError("Mirror {} not found in {}".format(
            mirror_name, mirror_entry.parent))

    mirror_mod = import_from_path(mirror_name, str(mirror_entry))
    solve_github_repo_url = mirror_mod.solve

    pspy_local_path = Path(STR_PY_PSC_LOCAL_PATH)
    ffi_deps = pspy_local_path / STR_FFI_DEPS_FILENAME
    with ffi_deps.open() as f:
        deps = f.read().splitlines()

    for dep in deps:
        parts = Path(dep).parts
        if len(parts) > 3 and parts[0] == '.spago':
            _, package_name, version_, *_ = parts
            version = [int(each)
                       for each in version_[1:].split('.')]  # type: List[int]

            # return a string, available at current machine
            yield solve_github_repo_url(package_name, version)


def build(run: bool = False, version: bool = False, init: bool = False, update: bool = False):
    """PureScript Python compiler"""
    path = Path().absolute()
    pure_py_conf = path / "pure-py.json"
    py_pack_name_default = path.name.replace('-', '_')
    if init:
        if not pure_py_conf.exists():
            with pure_py_conf.open('w') as f:
                json.dump(_TEMPLATE, f, indent=2, sort_keys=True)

            ignore_file = path / ".gitignore"
            with ignore_file.open('a+') as f:
                is_configured = {'.pure-py/': True, 'pure-py.json': True}
                for each in f.readlines():
                    if each in ('.pure-py/', 'pure-py.json'):
                        is_configured[each] = False

                xs = [k for k, v in is_configured.items() if v]
                if xs:
                    f.write('\n# purescript-python\n')
                    for x in xs:
                        f.write(x)
                        f.write('\n')

            local_dir = (path / STR_PY_PSC_LOCAL_PATH)
            local_dir.mkdir(parents=True, exist_ok=True)
            (local_dir / STR_FFI_DEPS_FILENAME).open('w').close()
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
    conf_dict.setdefault(CKey.Spago, CValue.Spago)
    conf_dict.setdefault(CKey.EntryModule, CValue.EntryModule)

    conf = CValue()
    conf.IndexMirror = conf_dict[CKey.IndexMirror]
    conf.BluePrint = conf_dict[CKey.BluePrint]
    conf.PyPack = conf_dict[CKey.PyPack]
    conf.CoreFnDir = conf_dict[CKey.CoreFnDir]
    conf.Spago = conf_dict[CKey.Spago]
    conf.EntryModule = conf_dict[CKey.EntryModule]

    # TODO: currently unused.
    #   support custom corefn output path in pspy-blueprint.
    corefn_dir = path / conf.CoreFnDir

    # run commands
    if run:
        sys.path.append(str(path))
        mod = import_module('{}.{}.pure'.format(conf.PyPack, conf.EntryModule))
        if hasattr(mod, 'main'):
            mod.main()
        return
    elif version:
        from purescripto.version import __version__
        print('{}'.format(__version__))
        return

    pspy_local_path = Path(STR_PY_PSC_LOCAL_PATH)

    if not pspy_local_path.exists():
        pspy_local_path.mkdir(parents=True)

    ffi_deps_file = pspy_local_path / STR_FFI_DEPS_FILENAME
    cmd = mk_ps_blueprint_cmd(conf.BluePrint, conf.PyPack, conf.EntryModule,
                              str(ffi_deps_file))
    check_call(cmd)

    path_join = os.path.join
    python_ffi_path = Path(conf.PyPack) / "ffi"
    if not python_ffi_path.exists():
        python_ffi_path.mkdir(parents=True)
    python_ffi_path = str(python_ffi_path)

    # copy python ffi files
    for repo_url in solve_ffi(conf):
        repo = auto_link_repo(repo_url, update=update)
        copy_tree(path_join(repo.working_dir, 'python-ffi'), python_ffi_path)

    python_ffi_provided_by_current_proj = path / "python-ffi"
    if python_ffi_provided_by_current_proj.exists():
        copy_tree(str(python_ffi_provided_by_current_proj), python_ffi_path)

    # fill __init__.py
    for dir, _, files in os.walk(conf.PyPack):
        if '__init__.py' not in files:
            open(path_join(dir, '__init__.py'), 'w').close()
