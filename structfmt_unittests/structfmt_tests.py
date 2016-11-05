import structfmt
import unittest


class StructFormatTests(unittest.TestCase):
    def test_without_params(self):
        fmt = (structfmt.struct_format()
               .bool()
               .byte()
               .bytes()
               .double()
               .float()
               .int8()
               .int16()
               .int32()
               .int64()
               .long()
               .native_pointer()
               .pascal_bytes()
               .size_t()
               .skip_bytes()
               .ssize_t()
               .uint8()
               .uint16()
               .uint32()
               .uint64()
               .ulong()).build_format_string()
        self.assertEqual('?csdfbhiqlPpNxnBHIQL', fmt)

    def test_with_params(self):
        fmt = (structfmt.struct_format()
               .bool(2)
               .byte(2)
               .bytes(2)
               .double(2)
               .float(2)
               .int8(2)
               .int16(2)
               .int32(2)
               .int64(2)
               .long(2)
               .native_pointer(2)
               .pascal_bytes(2)
               .size_t(2)
               .skip_bytes(2)
               .ssize_t(2)
               .uint8(2)
               .uint16(2)
               .uint32(2)
               .uint64(2)
               .ulong(2)).build_format_string()
        self.assertEqual('2?2c2s2d2f2b2h2i2q2l2P2p2N2x2n2B2H2I2Q2L', fmt)

    def fmt_string_should_be_short(self):
        fmt = (structfmt.struct_format()
               .int32()
               .int32()
               .int32()
               .int32()
               .bytes(2)
               .bytes(2)
               .bytes(2)
               .pascal_bytes(2)
               .pascal_bytes(3)
               .pascal_bytes(4)
               ).build_format_string()
        self.assertEqual('4i2b2b2b2p3p4p', fmt)

    def test_skip_to_offset(self):
        fmt = (structfmt.struct_format()
               .int16()
               .skip_to_offset(7)
               .int32()
               ).build_format_string()
        self.assertEqual('h5xi', fmt)


class StructNamedFormatTests(unittest.TestCase):
    def test_fmt_named(self):
        fmt = (structfmt.struct_named_format("name")
               .bool('bool1', 'bool2')
               .byte('byte1', 'byte2')
               .bytes('bytes', 2)
               .double('double1', 'double2')
               .float('float1', 'float2')
               .int8('int8-1', 'int8-2')
               .int16('int16-1', 'int16-2')
               .int32('int32-1', 'int32-2')
               .int64('int64-1', 'int64-2')
               .long('long1', 'long2')
               .native_pointer('ptr1', 'ptr2')
               .pascal_bytes('pascal', 2)
               .size_t('sizet1', 'sizet2')
               .skip_bytes(2)
               .ssize_t('ssizet1', 'ssizet2')
               .uint8('uint8-1', 'uint8-2')
               .uint16('uint16-1', 'uint16-2')
               .uint32('uint32-1', 'uint32-2')
               .uint64('uint64-1', 'uint64-2')
               .ulong('ulong1', 'ulong2')
               ).build_format_string()
        self.assertEqual('2?2c2s2d2f2b2h2i2q2l2P2p2N2x2n2B2H2I2Q2L', fmt)

    def test_namedtuple(self):
        s = (structfmt.struct_named_format("name")
             .little_endian()
             .int32("int1")
             .int32("int2")).build_formatted_struct()

        packed = s.pack(0x1234, 0x4321)
        self.assertEqual(b'\x34\x12\x00\x00\x21\x43\x00\x00', packed)

        unpacked = s.unpack(packed)
        self.assertEqual(0x1234, unpacked.int1)
        self.assertEqual(0x4321, unpacked.int2)

    def test_mapper(self):
        s = (structfmt.struct_named_format("name")
             .little_endian()
             .int32("int1")
             ._with_mapper(lambda x: str(x + 1))
             ).build_formatted_struct()

        packed = s.pack(1234)

        unpacked = s.unpack(packed)
        expected = str(1234 + 1)
        print(unpacked)
        self.assertEqual(expected, unpacked.int1)

    def test_ethernet(self):
        def bytes_to_mac_string(b):
            hexcode = list(map(lambda x: format(x, '02x'), b))
            return "{}:{}:{}:{}:{}:{}".format(*hexcode)

        packet_types = {
            0x0008: 'IPv4',
            0x0091: 'VlanTagged'
        }

        ethernet_frame = (
            structfmt.struct_named_format("Ethernet")
            .little_endian()
            .bytes("MacDestination", 6, mapper=bytes_to_mac_string)
            .bytes("MacSource", 6, mapper=bytes_to_mac_string)
            .int16("PacketType", mapper=lambda x: packet_types[x])
        ).build_formatted_struct()

        frame_in_bytes = b'\x80\x00\x20\x7a\x3f\x3e\x80\x00\x20\x20\x3a\xae\x08\x00'

        decoded = ethernet_frame.unpack(frame_in_bytes)
        self.assertEqual('80:00:20:7a:3f:3e', decoded.MacDestination)
        self.assertEqual('80:00:20:20:3a:ae', decoded.MacSource)
        self.assertEqual('IPv4', decoded.PacketType)
