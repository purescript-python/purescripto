def zfsr32(val, n):
    """zero fill shift right for 32 bit integers"""
    return (val >> n) if val >= 0 else ((val + 4294967296) >> n)
