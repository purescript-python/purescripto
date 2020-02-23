from contextlib import contextmanager
from py_sexpr import terms
import warnings

__metadata_to_wrap = terms.metadata
__define_to_wrap = terms.define


def define(name, args, body):
    r"https://github.com/purescript-python/purescript-python/issues/10"
    return __define_to_wrap(name, args, body, [None] * len(args))


def metadata(line, col, filename, sexpr):
    """https://github.com/purescript-python/purescript-python/issues/8
    """
    if line is 0:
        line = 1
    return __metadata_to_wrap(line, col, filename, sexpr)


# one of following approaches is okay


@contextmanager
def workaround():
    """contextually invoke this when loading *.src.py"""
    __metadata_to_wrap.__globals__['metadata'] = metadata
    __define_to_wrap.__globals__['define'] = define
    try:
        yield
    finally:
        __metadata_to_wrap.__globals__['metadata'] = __metadata_to_wrap
        __define_to_wrap.__globals__['define'] = __define_to_wrap


@contextmanager
def suppress_cpy38_literal_is():
    """https://github.com/purescript-python/purescript-python/issues/9"""
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',
                                category=SyntaxWarning,
                                message='"is" with a literal')
        yield
