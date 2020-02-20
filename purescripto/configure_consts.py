from pathlib import Path


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


STR_PSPY_BLUEPRINT_CMD = "pspy-blueprint"
STR_PY_PSC_LOCAL_PATH = '.pure-py'
STR_FFI_DEPS_FILENAME = 'ffi-deps'

PSPY_HOME = Path("~/.pspy").expanduser()
FFI_LOCAL_MODULE_PATH = PSPY_HOME / "ffi"

if not PSPY_HOME.exists():
    PSPY_HOME.mkdir(parents=True)
