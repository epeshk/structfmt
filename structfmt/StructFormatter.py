import struct


class StructFormatter:
    def __init__(self):
        self._byteorder = '@'
        self._parts = []
        self._offset = 0

    @property
    def offset(self):
        return self._offset

    def native_alignment_endian(self):
        """
        Sets native byte order with native fields alignment
        :rtype: StructFormatter
        """
        self._ensure_offsets('@')
        self._byteorder = '@'
        return self

    def native_endian(self):
        """
        Sets native byte order
        :rtype: StructFormatter
        """
        self._ensure_offsets('=')
        self._byteorder = '='
        return self

    def little_endian(self):
        """
        Sets Little Endian byte order
        :rtype: StructFormatter
        """
        self._ensure_offsets('<')
        self._byteorder = '<'
        return self

    def big_endian(self):
        """
        Sets Big Endian byte order
        :rtype: StructFormatter
        """
        self._ensure_offsets('>')
        self._byteorder = '>'
        return self

    def network_endian(self):
        """
        Sets network byte order
        :rtype: StructFormatter
        """
        self._ensure_offsets('!')
        self._byteorder = '!'
        return self

    def skip_bytes(self, count=1):
        """
        Skips bytes
        :param count: count of bytes to skip
        :rtype: StructFormatter
        """
        return self._add('x', count)

    def skip_to_offset(self, offset=0x01):
        """
        Skips bytes to specified offset
        :param offset: offset to move,
        should be greater than current offset.
        :rtype: StructFormatter
        """
        if offset < self._offset:
            raise ValueError("Offset to move should be greater"
                             "than current offset")
        return self.skip_bytes(offset - self._offset)

    def bool(self, count=1):
        """
        Boolean value
        c type: bool
        python type: bool
        :param count: number of bool values
        :rtype: StructFormatter
        """
        return self._add('?', count)

    def byte(self, count=1):
        """
        Char field
        c type: char
        python type: bytes of length 1
        :param count: count of bytes objects
        :rtype: StructFormatter
        """
        return self._add('c', count)

    def int8(self, count=1):
        """
        1 byte integer field
        c type: signed char
        python type: int
        :param count: cunt of fields
        :rtype: StructFormatter
        """
        return self._add('b', count)

    def uint8(self, count=1):
        """
        1 byte unsigned integer field
        c type: unsigned char
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('B', count)

    def int16(self, count=1):
        """
        2 bytes integer field
        c type: short
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('h', count)

    def uint16(self, count=1):
        """
        2 bytes unsigned integer field
        c type: unsigned short
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('H', count)

    def int32(self, count=1):
        """
        4 bytes integer field
        c type: int
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('i', count)

    def uint32(self, count=1):
        """
        4 bytes unsigned integer field
        c type: unsigned int
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('I', count)

    def int64(self, count=1):
        """
        8 bytes integer field
        c type: long long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('q', count)

    def uint64(self, count=1):
        """
        4 bytes unsigned integer field
        c type: unsigned long long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('Q', count)

    def long(self, count=1):
        """
        4 bytes integer field
        c type: long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('l', count)

    def ulong(self, count=1):
        """
        4 bytes unsigned integer field
        c type: long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('L', count)

    def ssize_t(self, count=1):
        """
        Platform specified signed integer field
        c type: ssize_t
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('n', count)

    def size_t(self, count=1):
        """
        Platform specified unsigned integer field
        c type: size_t
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('N', count)

    def half_precision(self, count=1):
        """
        2 bytes half precision IEEE754-2008 floating point number field
        c type: half (nonstandard)
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('e', count)

    def float(self, count=1):
        """
        4 bytes single precision IEEE754 floating point number field
        c type: float
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('f', count)

    def double(self, count=1):
        """
        8 bytes double precision IEEE754 floating point number field
        c type: double
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('d', count)

    def bytes(self, length=1):
        """
        Bytes sequence of specified length
        c type: char[]
        python type: bytes
        :param length: bytes sequence length
        :rtype: StructFormatter
        """
        return self._add('s', length)

    def pascal_bytes(self, max_length=1):
        """
        Bytes sequence. Length specified in first byte,
        so, max_length is not greater than min(max_length - 1, 255)
        c type: char[]
        python type: bytes
        :param max_length: max length of bytes sequence
        :rtype: StructFormatter
        """
        if max_length == 0:
            raise ValueError("incorrect length of pascal string")
        return self._add('p', max_length)

    def native_pointer(self, count=1):
        """
        Platform specified pointer integer field
        c type: (void*)
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self._add('P', count)

    def _ensure_offsets(self, byteorder):
        if not self._parts or (self._byteorder == byteorder):
            return
        if self._byteorder == '@' or byteorder == '@':
            raise ValueError("Alignment can't be changed after adding parts")

    def _add(self, symbol, count):
        if count < 0:
            raise ValueError("Incorrect fields count: " + str(count))
        if not self._parts or symbol in 'sp' or self._parts[-1][0] != symbol:
            self._parts.append([symbol, count])
        else:
            self._parts[-1][1] += count
        self._offset += struct.calcsize(str(count) + symbol)
        return self

    @staticmethod
    def _part_to_str(part):
        if part[1] == 1:
            return part[0]
        return str(part[1]) + part[0]

    def build_format_string(self):
        if self._byteorder == '@':
            return ''.join(map(self._part_to_str, self._parts))
        return self._byteorder + ''.join(map(self._part_to_str, self._parts))

    def build_struct(self):
        return struct.Struct(self.build_format_string())
