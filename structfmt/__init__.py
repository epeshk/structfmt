from collections import namedtuple
from .structfmt import struct_format, struct_named_format

__all__ = ['structfmt.struct_format',
           'structfmt.struct_named_format']


class FormattedStruct:
    def __init__(self, struct, nt, mappers):
        self._struct = struct
        self._nt = nt
        self._mappers = mappers

    @property
    def namedtuple(self):
        return self._nt

    @property
    def size(self):
        return self._struct.size

    def pack(self, *items):
        return self._struct.pack(*items)

    def pack_into(self, buffer, offset, *items):
        return self._struct.pack(buffer, offset, *items)

    def unpack(self, buffer):
        if not self._mappers:
            return self._nt(*self._struct.unpack(buffer))
        return self._nt._make(
            map(self._conv,
                zip(self._nt._fields,
                    self._struct.unpack(buffer))))

    def unpack_from(self, buffer, offset=0):
        # it can be reimplemented better with iter_unpack
        # but that is Python 3.4 feature
        if not self._mappers:
            return self._nt(*self._struct.unpack_from(buffer, offset))
        return self._nt._make(
            map(self._conv,
                zip(self._nt._fields,
                    self._struct.unpack_from(buffer, offset))))

    def iter_unpack(self, buffer):
        if not self._mappers:
            return self._struct.iter_unpack(buffer)
        return map(self._conv,
                   zip(self._nt._fields,
                       self._struct.iter_unpack(buffer)))

    def _conv(self, item):
        if item[0] in self._mappers:
            return self._mappers[item[0]](item[1])

        return item[1]


def create_nt(name, fields):
    return namedtuple(name, fields)
