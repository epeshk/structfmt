import struct


class StructFormatter:
    def __init__(self):
        self.__byteorder = '@'
        self.__parts = []
        self.__current = None
        self.__offset = 0

    @property
    def offset(self):
        return self.__offset

    def native_alignment_endian(self):
        """
        Sets native byte order with native fields alignment
        :rtype: StructFormatter
        """
        self.__ensure_offsets('@')
        self.__byteorder = '@'
        return self

    def native_endian(self):
        """
        Sets native byte order
        :rtype: StructFormatter
        """
        self.__ensure_offsets('=')
        self.__byteorder = '='
        return self

    def little_endian(self):
        """
        Sets Little Endian byte order
        :rtype: StructFormatter
        """
        self.__ensure_offsets('<')
        self.__byteorder = '<'
        return self

    def big_endian(self):
        """
        Sets Big Endian byte order
        :rtype: StructFormatter
        """
        self.__ensure_offsets('>')
        self.__byteorder = '>'
        return self

    def network_endian(self):
        """
        Sets network byte order
        :rtype: StructFormatter
        """
        self.__ensure_offsets('!')
        self.__byteorder = '!'
        return self

    def skip_bytes(self, count=1):
        """
        Skips bytes
        :param count: count of bytes to skip
        :rtype: StructFormatter
        """
        return self.__add('x', count)

    def skip_to_offset(self, offset=0x01):
        """
        Skips bytes to specified offset
        :param offset: offset to move,
        should be greater than current offset.
        :rtype: StructFormatter
        """
        if offset < self.__offset:
            raise ValueError("Offset to move should be greater"
                             "than current offset")
        return self.skip_bytes(offset - self.__offset)

    def bool(self, count=1):
        """
        Boolean value
        c type: bool
        python type: bool
        :param count: number of bool values
        :rtype: StructFormatter
        """
        return self.__add('?', count)

    def byte(self, count=1):
        """
        Char field
        c type: char
        python type: bytes of length 1
        :param count: count of bytes objects
        :rtype: StructFormatter
        """
        return self.__add('c', count)

    def int8(self, count=1):
        """
        1 byte integer field
        c type: signed char
        python type: int
        :param count: cunt of fields
        :rtype: StructFormatter
        """
        return self.__add('b', count)

    def uint8(self, count=1):
        """
        1 byte unsigned integer field
        c type: unsigned char
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('B', count)

    def int16(self, count=1):
        """
        2 bytes integer field
        c type: short
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('h', count)

    def uint16(self, count=1):
        """
        2 bytes unsigned integer field
        c type: unsigned short
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('H', count)

    def int32(self, count=1):
        """
        4 bytes integer field
        c type: int
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('i', count)

    def uint32(self, count=1):
        """
        4 bytes unsigned integer field
        c type: unsigned int
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('I', count)

    def int64(self, count=1):
        """
        8 bytes integer field
        c type: long long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('q', count)

    def uint64(self, count=1):
        """
        4 bytes unsigned integer field
        c type: unsigned long long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('Q', count)

    def long(self, count=1):
        """
        4 bytes integer field
        c type: long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('l', count)

    def ulong(self, count=1):
        """
        4 bytes unsigned integer field
        c type: long
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('L', count)

    def ssize_t(self, count=1):
        """
        Platform specified signed integer field
        c type: ssize_t
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('n', count)

    def size_t(self, count=1):
        """
        Platform specified unsigned integer field
        c type: size_t
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('N', count)

    def half_precision(self, count=1):
        """
        2 bytes half precision IEEE754-2008 floating point number field
        c type: half (nonstandard)
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('e', count)

    def float(self, count=1):
        """
        4 bytes single precision IEEE754 floating point number field
        c type: float
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('f', count)

    def double(self, count=1):
        """
        8 bytes double precision IEEE754 floating point number field
        c type: double
        python type: float
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('d', count)

    def bytes(self, length=1):
        """
        Bytes sequence of specified length
        c type: char[]
        python type: bytes
        :param length: bytes sequence length
        :rtype: StructFormatter
        """
        return self.__add('s', length)

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
        return self.__add('p', max_length)

    def native_pointer(self, count=1):
        """
        Platform specified pointer integer field
        c type: (void*)
        python type: int
        :param count: count of fields
        :rtype: StructFormatter
        """
        return self.__add('P', count)

    def __ensure_offsets(self, byteorder):
        if not self.__parts or (self.__byteorder == byteorder):
            return
        if self.__byteorder == '@' or byteorder == '@':
            raise ValueError("Alignment can't be changed after adding parts")

    def __add(self, symbol, count):
        if count < 0:
            raise ValueError("Incorrect fields count: " + str(count))
        if not self.__parts or symbol in 'sp' or self.__parts[-1][0] != symbol:
            self.__parts.append([symbol, count])
        else:
            self.__parts[-1][1] += count
        self.__offset += struct.calcsize(str(count) + symbol)
        return self

    @staticmethod
    def __part_to_str(part):
        if part[1] == 1:
            return part[0]
        return str(part[1]) + part[0]

    def build_format_string(self):
        if self.__byteorder == '@':
            return ''.join(map(self.__part_to_str, self.__parts))
        return self.__byteorder + ''.join(map(self.__part_to_str, self.__parts))

    def build_struct(self):
        return struct.Struct(self.build_format_string())
