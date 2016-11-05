import struct
from .StructFormatter import StructFormatter

top_package = __import__(__name__.split('.')[0])


class StructNamedFormatter:
    def __init__(self, name):
        self.__name = name
        self.__fields = []
        self.__mappers = {}
        self.__formatter = StructFormatter()

        self.__last_added_count = 0

    @property
    def offset(self):
        return self.__formatter.offset

    def native_alignment_endian(self):
        """
        Sets native byte order with native fields alignment
        :rtype: StructNamedFormatter
        """
        self.__formatter.native_alignment_endian()
        return self

    def native_endian(self):
        """
        Sets native byte order
        :rtype: StructNamedFormatter
        """
        self.__formatter.native_endian()
        return self

    def little_endian(self):
        """
        Sets Little Endian byte order
        :rtype: StructNamedFormatter
        """
        self.__formatter.little_endian()
        return self

    def big_endian(self):
        """
        Sets Big Endian byte order
        :rtype: StructNamedFormatter
        """
        self.__formatter.big_endian()
        return self

    def network_endian(self):
        """
        Sets network byte order
        :rtype: StructNamedFormatter
        """
        self.__formatter.network_endian()
        return self

    def skip_bytes(self, count=1):
        """
        Skips bytes
        :param count: count of bytes to skip
        :rtype: StructNamedFormatter
        """
        self.__formatter.skip_bytes(count)
        return self

    def skip_to_offset(self, offset=0x01):
        """
        Skips bytes to specified offset
        :param offset: offset to move,
        should be greater than current offset.
        :rtype: StructNamedFormatter
        """
        self.__formatter.skip_to_offset(offset)
        return self

    def bool(self, *fields, mapper=None):
        """
        Boolean value
        c type: bool
        python type: bool
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.bool(len(fields))
        return self

    def byte(self, *fields, mapper=None):
        """
        Char field
        c type: char
        python type: bytes of length 1
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.byte(len(fields))
        return self

    def int8(self, *fields, mapper=None):
        """
        1 byte integer field
        c type: signed char
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.int8(len(fields))
        return self

    def uint8(self, *fields, mapper=None):
        """
        1 byte unsigned integer field
        c type: unsigned char
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.uint8(len(fields))
        return self

    def int16(self, *fields, mapper=None):
        """
        2 bytes integer field
        c type: short
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.int16(len(fields))
        return self

    def uint16(self, *fields, mapper=None):
        """
        2 bytes unsigned integer field
        c type: unsigned short
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.uint16(len(fields))
        return self

    def int32(self, *fields, mapper=None):
        """
        4 bytes integer field
        c type: int
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.int32(len(fields))
        return self

    def uint32(self, *fields, mapper=None):
        """
        4 bytes unsigned integer field
        c type: unsigned int
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.uint32(len(fields))
        return self

    def int64(self, *fields, mapper=None):
        """
        8 bytes integer field
        c type: long long
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.int64(len(fields))
        return self

    def uint64(self, *fields, mapper=None):
        """
        4 bytes unsigned integer field
        c type: unsigned long long
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.uint64(len(fields))
        return self

    def long(self, *fields, mapper=None):
        """
        4 bytes integer field
        c type: long
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.long(len(fields))
        return self

    def ulong(self, *fields, mapper=None):
        """
        4 bytes unsigned integer field
        c type: long
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.ulong(len(fields))
        return self

    def ssize_t(self, *fields, mapper=None):
        """
        Platform specified signed integer field
        c type: ssize_t
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.ssize_t(len(fields))
        return self

    def size_t(self, *fields, mapper=None):
        """
        Platform specified unsigned integer field
        c type: size_t
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.size_t(len(fields))
        return self

    def half_precision(self, *fields, mapper=None):
        """
        2 bytes half precision IEEE754-2008 floating point number field
        c type: half (nonstandard)
        python type: float
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.half_precision(len(fields))
        return self

    def float(self, *fields, mapper=None):
        """
        4 bytes single precision IEEE754 floating point number field
        c type: float
        python type: float
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.float(len(fields))
        return self

    def double(self, *fields, mapper=None):
        """
        8 bytes double precision IEEE754 floating point number field
        c type: double
        python type: float
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.double(len(fields))
        return self

    def bytes(self, field, length, mapper=None):
        """
        Bytes sequence of specified length
        c type: char[]
        python type: bytes
        :param mapper: mapper func
        :param length: bytes sequence length
        :param field: field name
        :rtype: StructNamedFormatter
        """
        self.__add_fields([field], mapper)
        self.__formatter.bytes(length)
        return self

    def pascal_bytes(self, field, max_length=1, mapper=None):
        """
        Bytes sequence. Length specified in first byte,
        so, max_length is not greater than min(max_length - 1, 255)
        c type: char[]
        python type: bytes
        :param mapper: mapper func
        :param max_length: max length of bytes sequence
        :param field: field name
        :rtype: StructNamedFormatter
        """
        self.__add_fields([field], mapper)
        self.__formatter.pascal_bytes(max_length)
        return self

    def native_pointer(self, *fields, mapper=None):
        """
        Platform specified pointer integer field
        c type: (void*)
        python type: int
        :param mapper: mapper func
        :rtype: StructNamedFormatter
        """
        self.__add_fields(fields, mapper)
        self.__formatter.native_pointer(len(fields))
        return self

    def _with_mapper(self, mapper_func, *fields):
        """
        :param mapper_func: func that maps
        values from internal view
        :rtype: StructNamedFormatter
        """
        if not fields:
            fields = self.__fields[-self.__last_added_count:]
        for field in fields:
            self.__mappers[field] = mapper_func
        return self

    def __add_fields(self, fields, mapper=None):
        prev_len = len(self.__fields)
        self.__fields += fields
        self.__last_added_count = len(self.__fields) - prev_len
        if mapper:
            self._with_mapper(mapper)

    def build_format_string(self):
        return self.__formatter.build_format_string()

    def build_formatted_struct(self):
        """

        :rtype: FormattedStruct
        """
        s = struct.Struct(self.build_format_string())
        nt = top_package.create_nt(self.__name, self.__fields)
        return top_package.FormattedStruct(s, nt, self.__mappers)
