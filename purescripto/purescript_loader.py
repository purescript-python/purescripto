from pathlib import Path
from typing import Union, Tuple
from types import CodeType
from pie import LoaderForBetterLife
from importlib import import_module
from purescripto import rts
from purescripto.utilities import import_from_path
from purescripto.workaround import suppress_cpy38_literal_is, workaround
from py_sexpr.stack_vm.emit import module_code
from purescripto.topdown import load_topdown
import marshal
import zipfile
import io
import functools

RES = "res"
"""generated code object is stored in global variable $RES"""


@functools.lru_cache()
def _import_module_to_dict(m: str):
    with suppress_cpy38_literal_is():
        package, _, module = m.rpartition(".")
        entry_path = import_module(package).__file__
        loc = entry_path[: -len("__init__.py")] + module + ".py"
        return import_from_path(m, loc).__dict__


RTS_TEMPLATE = {
    "zfsr32": rts.zfsr32,
    "Error": Exception,
    "import_module": _import_module_to_dict,
}


def _META_ENV():
    with workaround():
        import py_sexpr.terms as terms

        def make_pair(a, b):
            return a, b

        env = {each: getattr(terms, each) for each in terms.__all__}
        env[make_pair.__name__] = make_pair
    return env


META_ENV = _META_ENV()


class LoadPureScriptImplCode(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path) -> CodeType:

        filename = str(path.absolute())
        if path.name.endswith(".raw.py"):
            meta_code = compile(src, filename, "eval")
            sexpr = eval(meta_code, META_ENV)
        else:
            assert path.name.endswith(".zip.py")
            zip = zipfile.ZipFile(filename)
            file = io.StringIO(zip.read('source').decode('utf8'))
            sexpr = load_topdown(file, META_ENV)

        code = module_code(sexpr, name=self.qualified_name + "$", filename=filename)
        return code

    def load_program(self, b: bytes) -> CodeType:
        return marshal.loads(b)

    def dump_program(self, prog: CodeType) -> bytes:
        return marshal.dumps(prog)

    def suffix(self) -> Union[str, Tuple[str, ...]]:
        return ".raw.py", ".zip.py"


def LoadPureScript(file: str, name: str):
    loader = LoadPureScriptImplCode(file, name)
    code = loader.load()
    man_made_globals = RTS_TEMPLATE.copy()
    exec(code, man_made_globals)
    return man_made_globals["exports"]
