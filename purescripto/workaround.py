from contextlib import contextmanager
from py_sexpr import terms
import warnings


def metadata(line, col, filename, sexpr):
    """https://github.com/purescript-python/purescript-python/issues/8
    """
    if line is 0:
        line = 1
    return terms.metadata(line, col, filename, sexpr)


# one of following approaches is okay
terms.metadata.__globals__['metadata'] = metadata
setattr(terms, 'metadata', metadata)


@contextmanager
def suppress_cpy38_literal_is():
    """https://github.com/purescript-python/purescript-python/issues/9"""
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',
                                category=SyntaxWarning,
                                message='"is" with a literal')
        yield
