# <pep8 compliant>

"""
"""

from array import array
from struct import pack_into, unpack_from
from sys import maxsize
from typing import Union


def ArrayBuffer(length=0):
    # type: (Union[float, int]) -> array
    """
    Represents a raw buffer of binary data, which is used to store data for the
    different typed arrays. ArrayBuffers cannot be read from or written to directly,
    but can be passed to a typed array or DataView Object to interpret the raw
    buffer as needed.

    :param length: The size, in bytes, of the array buffer to create.
    :type length: Union[`float`, `int`]

    :return: Array of the specified size. Its contents are initialized to 0.
    :rtype: `array`
    """
    if not isinstance(length, (float, int)):
        length = 0
    elif 0 > length > maxsize:
        raise ValueError("Invalid array buffer length")

    return array('B', bytes(int(length)))


class DataView:
    """
    """

    __slots__ = ("_bytes_buffer", "_bytes_length", "_bytes_offset")

    _bytes_buffer: array
    _bytes_length: int
    _bytes_offset: int

    def __init__(self, buffer, byteOffset=0, byteLength=None):
        # type: (array, Union[float, int], Union[float, int, None]) -> None

        # PARAM CHECK: BUFFER
        if not isinstance(buffer, array):
            raise TypeError("First argument to DataView constructor must be an ArrayBuffer")

        # PARAM CHECK: BYTEOFFSET
        if not isinstance(byteOffset, (float, int)):
            byteOffset = 0
        elif len(buffer) <= byteOffset < 0:
            raise IndexError(f"Start offset {int(byteOffset)} is outside the bounds of the buffer")

        # PARAM CHEECK: BYTELENGTH
        if not isinstance(byteLength, (float, int)):
            byteLength = len(buffer)
        elif (byteLength < 0) or (len(buffer) < (byteOffset + byteLength)):
            raise IndexError(f"Invalid DataView length {int(byteLength)}")

        self._bytes_buffer = buffer
        self._bytes_length = int(byteLength)
        self._bytes_offset = int(byteOffset)

    @property
    def buffer(self):
        # type: () -> array
        return self._bytes_buffer

    @property
    def byteLength(self):
        # type: () -> int
        return self._bytes_length

    @property
    def byteOffset(self):
        # type: () -> int
        return self._bytes_offset

    def _get_value(self, offset, t_chr, t_len):
        # type: (Union[float, int], str, int) -> Union[float, int]

        # PARAM CHECK: BYTE OFFSET
        if not isinstance(offset, (float, int)):
            offset = 0
        elif (offset < 0) or (self._bytes_length <= (self._bytes_offset + offset + t_len)):
            raise IndexError("Offset is outside the bounds of the DataView")

        return unpack_from(t_chr, self._bytes_buffer, self._bytes_offset + offset)[0]

    def _set_value(self, offset, value, t_chr, t_len, t_min, t_max):
        # type: (int, Union[float, int], str, int, Union[float, int], Union[float, int]) -> None

        # PARAM CHECK: BYTE OFFSET
        if not isinstance(offset, (float, int)):
            offset = 0
        elif (offset < 0) or (self._bytes_length <= (self._bytes_offset + offset + t_len)):
            raise IndexError("Offset is outside the bounds of the DataView")

        # PARAM CHECK: VALUE
        if not isinstance(value, (float, int)):
            value = 0
        elif t_min > value > t_max:
            value %= t_max + 1

        pack_into(t_chr, self._bytes_buffer, self._bytes_offset + offset, value)

    def getBigInt64(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `BigInt64` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `BigInt64` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<q' if littleEndian else '>q', 8)

    def getBigUint64(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `BigUint64` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `BigUint64` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<Q' if littleEndian else '>Q', 8)

    def getFloat32(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> float
        """
        Gets the `Float32` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `float`
        :return: `Float32` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<f' if littleEndian else '>f', 4)

    def getFloat64(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> float
        """
        Gets the `Float64` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `float`
        :return: `Float64` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<d' if littleEndian else '>d', 8)

    def getInt8(self, byteOffset):
        # type: (int) -> int
        """
        Gets the `Int8` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Int8` value at the specified byte offset.
        """
        return self._get_value(byteOffset, 'b', 1)

    def getInt16(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `Int16` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Int16` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<h' if littleEndian else '>h', 2)

    def getInt32(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `Int32` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Int32` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<i' if littleEndian else '>i', 4)

    def getUint8(self, byteOffset):
        # type: (int) -> int
        """
        Gets the `Uint8` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Uint8` value at the specified byte offset.
        """
        return self._get_value(byteOffset, 'B', 1)

    def getUint16(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `Uint16` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Uint16` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<H' if littleEndian else '>H', 2)

    def getUint32(self, byteOffset, littleEndian=False):
        # type: (int, bool) -> int
        """
        Gets the `Uint32` value at the specified byte offset from the start of the view. There is
        no alignment constraint; multi-byte values may be fetched from any offset.

        :param byteOffset: The place in the buffer at which the value should be retrieved.
        :type  byteOffset: `int`
        :param littleEndian: If false or undefined, a big-endian value should be read, otherwise a
        little-endian value should be read.
        :type  littleEndian: `bool`
        :rtype: `int`
        :return: `Uint32` value at the specified byte offset.
        """
        return self._get_value(byteOffset, '<I' if littleEndian else '>I', 4)

    def setBigInt64(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `BigInt64` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<q' if littleEndian else '>q', 8,
                               -9223372036854775808, 9223372036854775807)

    def setBigUint64(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `BigUint64` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<Q' if littleEndian else '>Q', 8, 0,
                               18446744073709551615)

    def setFloat32(self, byteOffset, value, littleEndian=False):
        # type: (int, float, bool) -> None
        """
        Stores an `Float32` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `float`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<f' if littleEndian else '>f', 4,
                               -3.40282346638528859e+38, 3.40282346638528859e+38)

    def setFloat64(self, byteOffset, value, littleEndian=False):
        # type: (int, float, bool) -> None
        """
        Stores an `Float64` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `float`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<d' if littleEndian else '>d', 8,
                               -1.7976931348623157e+308, 1.7976931348623157e+308)

    def setInt8(self, byteOffset, value):
        # type: (int, int) -> None
        """
        Stores an `Int8` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        """
        return self._set_value(byteOffset, value, 'b', 1, -128, 127)

    def setInt16(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `Int16` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<h' if littleEndian else '>h', 2, -32768, 32767)

    def setInt32(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `Int32` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<i' if littleEndian else '>i', 4, -2147483648,
                               2147483647)

    def setUint8(self, byteOffset, value):
        # type: (int, int) -> None
        """
        Stores an `Uint8` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        """
        return self._set_value(byteOffset, value, 'B', 1, 0, 255)

    def setUint16(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `Uint16` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<H' if littleEndian else '>H', 2, 0, 65535)

    def setUint32(self, byteOffset, value, littleEndian=False):
        # type: (int, int, bool) -> None
        """
        Stores an `Uint32` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        :param littleEndian: If false or undefined, a big-endian value should be written,
        otherwise a little-endian value should be written.
        :type littleEndian: `bool`
        """
        return self._set_value(byteOffset, value, '<I' if littleEndian else '>I', 4, 0, 4294967295)
