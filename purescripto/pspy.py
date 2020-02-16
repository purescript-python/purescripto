from pathlib import Path
from importlib import import_module
from typing import Dict
from subprocess import check_call
import glob
import json

_pspy_hs_command = "pspy-one-module"


def cli(path: str, run: bool = False, version: bool = False):
    """PureScript Python compiler"""
    path = Path(path).absolute()
    _python_pack_name = path.parent
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


def main():
    import wisepy2
    wisepy2.wise(cli)()
