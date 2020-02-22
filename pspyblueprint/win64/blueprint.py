import sys
from pathlib import Path
from pspyblueprint.blueprint_impl import mk_call
exec_path = Path(__file__).parent / "pspy-blueprint.exe"
_call = mk_call(str(exec_path))


def main():
    _call(*sys.argv[1:])
