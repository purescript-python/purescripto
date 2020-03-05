from pathlib import Path
from typing import Union, Tuple
from types import CodeType
from pie import LoaderForBetterLife
from py_sexpr.stack_vm.emit import module_code
from purescripto.topdown import load_topdown
from purescripto.rts import META_ENV, RTS_TEMPLATE
import marshal
import zipfile
import io
import sys

class LoadPureScriptImplCode(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path) -> CodeType:
        sys.setrecursionlimit(3000)
        filename = str(path.absolute())
        if path.name.endswith(".raw.py"):
            meta_code = compile(src, filename, "eval")
            sexpr = eval(meta_code, META_ENV)
        else:
            assert path.name.endswith(".zip.py")
            zip = zipfile.ZipFile(filename)
            file = io.StringIO(zip.read("source").decode("utf8"))
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
