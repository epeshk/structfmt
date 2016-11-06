## structfmt

Python lib for easy work with binary struct in Fluent API style

### Features

* Creates format string for byte structures with fluent-like code
* Create FormattedStruct's which similar to struct.Struct's, but create namedtuples on unpack
* Map unpacked values by user defined mappers functions

#### Interface
```python
struct_format() # returns StructFormatter for build format string
struct_named_formatter() # returns StructNamedFormatter for build FormattedStruct

# Bytes ordering:
    .native_alignment_endian()
    .native_endian()
    .little_endian()
    .big_endian()
    .network_endian()

# Supported types:
    .bool()
    .byte()
    .bytes()
    .double()
    .float()
    .int8()
    .int16()
    .int32()
    .int64()
    .long() # C-long, similar to int32 !!!
    .native_pointer()
    .pascal_bytes() #array of bytes which first element defines array length
    .size_t()
    .ssize_t()
    .uint8()
    .uint16()
    .uint32()
    .uint64()
    .ulong() #C-unsigned long, similar to uint32 !!!

    .half_precision() # Python 3.6 feature

    .skip_bytes(n) - skips n bytes
    .skip_to_offset(offset) - skips all bytes to specified offset_
```

##### FormattedStruct interface
Behaviour similar to struct.Struct
```python
   pack(self, *items):
   pack_into(self, buffer, offset, *items):
   unpack(self, buffer):
   unpack_from(self, buffer, offset=0):
   iter_unpack(self, buffer):
   size
```

#### Examples:

##### StructFormatter

Create format string defines bytes represents two int32 and one int64 numbers, and array of 3 bytes with little endian byte order

```python
# [int32][int32][int64][array:[byte][byte][byte]]
import structfmt


format_string = (
    structfmt.struct_format()
    .little_endian()
    .int32(2) # 2 - count of fields of type int32
    .uint64()
    ).build_format_string()

print(format_string) #prints: "<2iQ"
```
##### StructNamedFormatter
Create formatted struct with two int32 fields and one int8 field
```python
# [int32][int8]
import structfmt


s = (structfmt.struct_named_format("name")
     .little_endian()
     .int32("width", "height") # specify names of int32 fields
     .int8("color") # all names must be unique!
     ).build_formatted_struct()

packed = s.pack(123, 456, 2)
unpacked = s.unpack(packed)

print(unpacked.width) # prints '123'
print(unpacked.height) # prints '456'
print(unpacked.color) # prints '2'
```

##### Mapper
Create formatted struct with two int32 fields and one int8 field. Set mapper for last field
```python
import structfmt


colors = {
    1 : "Red",
    2 : "Green",
    3 : "Blue"
}

byte_to_color = lambda x: colors[x]

s = (structfmt.struct_named_format("name")
     .little_endian()
     .int32("width", "height")
     .int8("color", mapper=byte_to_color)
     ).build_formatted_struct()

packed = s.pack(123, 456, 2)
unpacked = s.unpack(packed)

print(unpacked.width) # prints '123'
print(unpacked.height) # prints '456'
print(unpacked.color) # prints 'Green'
```

#### Ethernet frame
Parse begin of Ethernet frame, contains two Mac addresses and Frame type. Use mappers.
```python
import structfmt


# returns string which represents MAC-address by sequence of 6 bytes
def bytes_to_mac_string(b): 
    hexcode = list(map(lambda x: format(x, '02x'), b))
    return "{}:{}:{}:{}:{}:{}".format(*hexcode)

packet_types = {
    0x0008: 'IPv4',
    0x0091: 'VlanTagged'
  }

# define FormattedStruct represents begin of Ethernet frame
ethernet_frame = (
    structfmt.struct_named_format("Ethernet")
    .little_endian()
    .bytes("MacDestination", 6, mapper=bytes_to_mac_string)
    .bytes("MacSource", 6, mapper=bytes_to_mac_string)
    .int16("PacketType", mapper=lambda x: packet_types[x])
).build_formatted_struct()

frame_in_bytes = b'\x80\x00\x20\x7a\x3f\x3e\x80\x00\x20\x20\x3a\xae\x08\x00'

decoded = ethernet_frame.unpack(frame_in_bytes)
print(decoded.MacDestination) # prints '80:a0:20:7a:3f:3e'
print(decoded.MacSource) # prints '80:6a:24:20:3a:ae'
print(decoded.PacketType) # prints 'IPv4'
```

