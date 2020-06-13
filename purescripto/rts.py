from purescripto.utilities import import_from_path
from purescripto.workaround import suppress_cpy38_literal_is, workaround
from importlib import import_module
import functools
from py_sexpr.terms import *


def zfsr32(val, n):
    """zero fill shift right for 32 bit integers"""
    return (val >> n) if val >= 0 else ((val + 4294967296) >> n)


__all__ = ["META_ENV", "RTS_TEMPLATE"]


def _META_ENV():
    with workaround():
        import py_sexpr.terms as terms

        def make_pair(a, b):
            return a, b

        env = {each: getattr(terms, each) for each in terms.__all__}
        env[make_pair.__name__] = make_pair

    return env


@functools.lru_cache()
def _import_module_to_dict(m: str):
    with suppress_cpy38_literal_is():
        package, _, module = m.rpartition(".")
        entry_path = import_module(package).__file__
        loc = entry_path[: -len("__init__.py")] + module + ".py"
        return import_from_path(m, loc).__dict__


def getitem_looper(depth, base, item):
    while depth > 0:
        base = base[item]
        depth -= 1
    return base


def getattr_looper(depth, base, attr):
    # TODO: specializer here
    while depth > 0:
        base = get_attr(base, attr)
        depth -= 1
    return base


RTS_TEMPLATE = {
    "zfsr32": zfsr32,
    "Error": Exception,
    "import_module": _import_module_to_dict,
    getattr_looper.__name__: getattr_looper,
    getitem_looper.__name__: getitem_looper,
}


META_ENV = _META_ENV()
