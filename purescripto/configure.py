from pathlib import Path
from importlib import import_module
from typing import Dict, Optional, List, Tuple
from subprocess import check_call, check_output
import glob
import json
import sys

_pspy_hs_command = "pspy-one-module"
_pspy_local_dir = ".pspy"


def list_ffi_requirements(
        conf: Optional[dict]) -> List[Tuple[str, List[int], List[str]]]:
    """:return: [(PackageName, VersionParts, QualifiedModuleNames)]
    """
    if conf:
        spago_cmd = conf.get("spago", 'spago')
    else:
        spago_cmd = "spago"

    xs = check_output([spago_cmd, 'sources'])
    if not xs:
        raise IOError("spago command failed")
    package_paths = xs.decode().splitlines()

    packages_requiring_ffi = []

    for package_path in package_paths:
        package_path = Path(package_path)

        parts = package_path.parts
        if len(parts) > 3 and parts[0] == '.spago':
            # check if '.spago/<package name>/v<version>/src/**/*.purs
            _, package_name, version_, *_ = parts
            version = [int(each)
                       for each in version_[1:].split('.')]  # type: List[int]
        else:
            continue

        modules_requiring_ffi = []
        for js_file in glob.glob(str(package_path.parent / "**.js"),
                                 recursive=True):
            js_path = Path(js_file)
            if js_path.with_suffix(".purs").exists():
                # e.g.,
                #  from "ppt/.spago/console/v4.4.0\\src\\Effect\\Console.js"
                #  to "Effect/Console"
                module_parts = js_path.with_suffix("").parts[4:]
                modules_requiring_ffi.append('.'.join(module_parts))
        packages_requiring_ffi.append(
            (package_name, version, modules_requiring_ffi))
    return packages_requiring_ffi


def build(run: bool = False, version: bool = False):
    """PureScript Python compiler"""
    path = Path().absolute()
    _python_pack_name = path.name.replace('-', '_')
    corefn_dir = path / "output"
    pure_py_conf = path / "pure-py.json"
    if not pure_py_conf.exists():
        pspy_hs_command = _pspy_hs_command
        python_pack_name = _python_pack_name
        foreign_path = path / "src"
    else:
        with pure_py_conf.open() as f:
            conf = json.load(f)  # type: Dict[str, str]
        pspy_hs_command = conf.get('haskell-codegen', _pspy_hs_command)
        python_pack_name = conf.get('python-package', _python_pack_name)
        foreign_path = conf.get('python-ffi', None)
        if not foreign_path:
            foreign_path = path / "src"
        else:
            foreign_path = Path(foreign_path)

    if run:
        sys.path.append(str(path))
        import_module('{}.Main.purescript_impl'.format(python_pack_name))
        return
    elif version:
        from purescripto.version import __version__
        print('{}'.format(__version__))
        return
    python_pack_path = path / python_pack_name

    str_of_python_pack_path = str(python_pack_path)
    str_of_foreign_path = str(foreign_path)
    corefn_files = glob.glob(str(corefn_dir / "**" / "corefn.json"))
    for each in corefn_files:
        check_call([
            pspy_hs_command, '--foreign-top', str_of_foreign_path, '--out-top',
            str_of_python_pack_path, '--corefn', each
        ])
