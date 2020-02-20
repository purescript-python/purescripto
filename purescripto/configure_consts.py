class CKey:
    IndexMirror = 'index-mirror'
    Spago = 'spago'
    BluePrint = 'pspy-blueprint'
    PyPack = 'python-package'
    CoreFnDir = 'corefn-dir'
    EntryModule = 'entry-module'


class CValue:
    IndexMirror = 'default'
    Spago = 'spago'
    BluePrint = 'pspy-blueprint'
    PyPack = "python"
    CoreFnDir = 'output'
    EntryModule = 'Main'


PSPY_BLUEPRINT_CMD = "pspy-blueprint"
FFI_LOCAL_MODULE_PATH = "ffi"
PY_PSC_LOCAL_PATH = '.py-pure'
FFI_DEPS_FILENAME = 'ffi-deps'

PSPY_HOME = "~/.pspy"
