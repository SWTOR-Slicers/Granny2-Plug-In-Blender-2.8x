# <pep8 compliant>

from io import BufferedRandom, BufferedReader, BufferedWriter
from struct import pack, unpack
from typing import Union


class DataView:

    _buffer: Union[BufferedRandom, BufferedReader, BufferedWriter]
    _byteLength: int
    _byteOffset: int

    def __init__(self, buffer, byteOffset=0, byteLength=None):
        # type: (Union[BufferedReader, BufferedWriter], int, Union[int, None]) -> None

        # Buffer
        if isinstance(buffer, (BufferedRandom, BufferedReader, BufferedWriter)):
            if buffer.seekable():
                bufferData = buffer
            else:
                raise ValueError()
        else:
            raise TypeError()

        bufferSize = buffer.seek(0, 2) + 1

        # ByteOffset
        if isinstance(byteOffset, int):
            if 0 <= byteOffset < bufferSize:
                offset = byteOffset
            else:
                raise IndexError()
        else:
            raise TypeError()

        # ByteLength
        if byteLength is None:
            length = bufferSize - offset
        elif isinstance(byteLength, int):
            if (0 <= byteLength) and ((offset + byteLength) < bufferSize):
                length = byteLength
            else:
                raise ValueError()
        else:
            raise TypeError()

        # Store the values
        self._buffer = bufferData
        self._byteOffset = offset
        self._byteLength = length

    @property
    def buffer(self):
        # type: () -> Union[BufferedRandom, BufferedReader, BufferedWriter]
        return self._buffer

    @property
    def byteLength(self):
        # type: () -> int
        return self._byteLength

    @property
    def byteOffset(self):
        # type: () -> int
        return self._byteOffset

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
        buffer = self.buffer
        elem_size = 8

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<q' if bool(littleEndian) else '>q'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 8

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<Q' if bool(littleEndian) else '>Q'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 4

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<f' if bool(littleEndian) else '>f'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 8

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<d' if bool(littleEndian) else '>d'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 1

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        buffer.seek(offset)

        return unpack('b', buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 2

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<h' if bool(littleEndian) else '>h'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 4

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<i' if bool(littleEndian) else '>i'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 1

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        buffer.seek(offset)

        return unpack('B', buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 2

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<H' if bool(littleEndian) else '>H'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer
        elem_size = 4

        if not buffer.readable():
            raise RuntimeError()

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0 or self.byteLength <= (byteOffset + elem_size):
                raise IndexError()
        else:
            raise TypeError()

        offset = self.byteOffset + byteOffset

        # LittleEndian
        fmt_str = '<I' if bool(littleEndian) else '>I'

        buffer.seek(offset)

        return unpack(fmt_str, buffer.read(elem_size))[0]

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 9223372036854775807 < value < -9223372036854775808:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<q' if bool(littleEndian) else '>q'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 18446744073709551615 < value < 0:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<Q' if bool(littleEndian) else '>Q'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, float):
            if 3.40282346638528859e+38 < value < -3.40282346638528859e+38:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<f' if bool(littleEndian) else '>f'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, float):
            if 1.7976931348623157E+308 < value < -1.7976931348623157E+308:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<d' if bool(littleEndian) else '>d'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

    def setInt8(self, byteOffset, value):
        # type: (int, int) -> None
        """
        Stores an `Int8` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        """
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 127 < value < -128:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack('b', value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 32767 < value < -32768:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<h' if bool(littleEndian) else '>h'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 2147483647 < value < -2147483648:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<i' if bool(littleEndian) else '>i'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

    def setUint8(self, byteOffset, value):
        # type: (int, int) -> None
        """
        Stores an `Uint8` value at the specified byte offset from the start of the view.

        :param byteOffset: The place in the buffer at which the value should be set.
        :type byteOffset: `int`
        :param value: The value to set.
        :type value: `int`
        """
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 255 < value < 0:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack('B', value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 65535 < value < 0:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<H' if bool(littleEndian) else '>H'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))

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
        buffer = self.buffer

        if not buffer.writable():
            raise RuntimeError()    # TODO: Error Message

        # ByteOffset
        if isinstance(byteOffset, int):
            if byteOffset < 0:
                raise IndexError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        offset = self.byteOffset + byteOffset

        # Value
        if isinstance(value, int):
            if 4294967295 < value < 0:
                raise ValueError()  # TODO: Error Message
        else:
            raise TypeError()       # TODO: Error Message

        # LittleEndian
        fmt_str = '<I' if bool(littleEndian) else '>I'

        if byteOffset > (self.byteLength - 1):
            buffer.seek(0, 2)
            self._byteLength += buffer.write(bytes(byteOffset - (self.byteLength - 1)))

        buffer.seek(offset)
        buffer.write(pack(fmt_str, value))
