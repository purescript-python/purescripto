from pathlib import Path
from typing import Union, Tuple
from types import CodeType
from pie import LoaderForBetterLife
from importlib.util import spec_from_file_location, module_from_spec
import pickle

RES = 'res'
"""generated code object is stored in global variable $RES"""


class LoadPureScriptImplCode(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path) -> CodeType:
        spec = spec_from_file_location(self.qualified_name + '$',
                                       str(path.absolute()))
        mod = module_from_spec(spec)
        return getattr(mod, RES)

    def load_program(self, b: bytes) -> CodeType:
        return pickle.loads(b)

    def dump_program(self, prog: CodeType) -> bytes:
        return pickle.dumps(prog)

    def suffix(self) -> Union[str, Tuple[str, ...]]:
        return '.src.py'


def LoadPureScript(name: str, file: str):
    loader = LoadPureScriptImplCode(name, file)
    code = loader.load()
    man_made_globals = {}
    exec(code, man_made_globals)
    return man_made_globals['exports']
