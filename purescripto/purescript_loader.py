from pathlib import Path
from typing import Union, Tuple
from types import CodeType
from pie import LoaderForBetterLife
from importlib import import_module
from purescripto import rts
from purescripto.utilities import import_from_path
from purescripto.workaround import suppress_cpy38_literal_is, workaround
import marshal
import functools

RES = 'res'
"""generated code object is stored in global variable $RES"""


@functools.lru_cache()
def _import_module_to_dict(m: str):
    with suppress_cpy38_literal_is():
        package, _, module = m.rpartition('.')
        entry_path = import_module(package).__file__
        loc = entry_path[:-len('__init__.py')] + module + '.py'
        return import_from_path(m, loc).__dict__


RTS_TEMPLATE = {
    'zfsr32': rts.zfsr32,
    'Error': Exception,
    'import_module': _import_module_to_dict
}


class LoadPureScriptImplCode(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path) -> CodeType:
        with workaround():
            mod = import_from_path(self.qualified_name + '$',
                                   str(path.absolute()))
        return getattr(mod, RES)

    def load_program(self, b: bytes) -> CodeType:
        return marshal.loads(b)

    def dump_program(self, prog: CodeType) -> bytes:
        return marshal.dumps(prog)

    def suffix(self) -> Union[str, Tuple[str, ...]]:
        return '.src.py'


def LoadPureScript(file: str, name: str):
    loader = LoadPureScriptImplCode(file, name)
    code = loader.load()
    man_made_globals = RTS_TEMPLATE.copy()
    exec(code, man_made_globals)
    return man_made_globals['exports']
