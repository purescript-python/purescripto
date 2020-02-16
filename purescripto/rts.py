def Error(msg, self=None):
    return Exception(msg)


def zfsr64(val, n):
    """zero fill shift right for 64 bit integers"""
    return (val >> n) if val >= 0 else ((val + 0x10000000000000000) >> n)
