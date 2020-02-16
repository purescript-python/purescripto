from pathlib import Path
from typing import Union, Tuple
from types import CodeType
from pie import LoaderForBetterLife
from importlib.util import spec_from_file_location, module_from_spec
from importlib import import_module
from purescripto import rts
import marshal

RES = 'res'
"""generated code object is stored in global variable $RES"""

RTS_TEMPLATE = {
    'zfsr64': rts.zfsr64,
    'Error': rts.Error,
    'import_module': import_module
}


class LoadPureScriptImplCode(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path) -> CodeType:
        spec = spec_from_file_location(self.qualified_name + '$',
                                       str(path.absolute()))
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
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
