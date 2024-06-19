# <pep8 compliant>

from struct import pack, unpack


def decodeHalfFloat(arg):
    # type: (int) -> float
    return unpack('<e', pack('<H', arg))[0]


def encodeHalfFloat(arg):
    # type: (float) -> int
    return unpack('<H', pack('<e', arg))[0]
