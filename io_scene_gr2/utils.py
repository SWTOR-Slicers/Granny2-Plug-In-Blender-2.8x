# <pep8 compliant>

"""Common utility functions for parsing binary files."""

from struct import unpack


def rbytes(file, size):
    file.seek(size, 1)


def ruint8(file):  # Function to read unsigned byte
    return unpack(b'B', file.read(1))[0]


def rfloat8(file):  # Function to read a float that's been encoded as a single byte
    return float((unpack(b'B', file.read(1))[0] - 127.5) / 127.5)


def ruint16(file):  # Function to read unsigned int16
    return unpack(b'<H', file.read(2))[0]


def rfloat16(file):  # Function to read float16
    return unpack(b'<e', file.read(2))[0]


def rint32(file):  # Function to read signed int32
    return unpack(b'<i', file.read(4))[0]


def ruint32(file):  # Function to read unsigned int32
    return unpack(b'<I', file.read(4))[0]


def rfloat32(file):  # Function to read float32
    return unpack(b'<f', file.read(4))[0]


def rstring(file):
    offset = file.tell()

    file.seek(unpack(b'<I', file.read(4))[0])

    string = ""
    byte = file.read(1)

    while byte != b'\x00':
        string += byte.decode('utf-8')
        byte = file.read(1)

    file.seek(offset + 4)

    return string


def rcstring(file):
    string = ""
    byte = file.read(1)

    while byte != b'\x00':
        string += byte.decode('utf-8')
        byte = file.read(1)

    return string
