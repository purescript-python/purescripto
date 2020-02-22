import sys
from pathlib import Path
from pspyblueprint.blueprint_wrap import mk_call
exec_path = Path(__file__).parent / "pspy-blueprint"
_call = mk_call(str(exec_path))


def main():
    _call(*sys.argv[1:])
