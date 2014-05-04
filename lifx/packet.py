from collections import namedtuple
from struct import pack, unpack, calcsize

from lifx.packet_type import PacketType

class Packet:

    header = 'size protocol reserved1 target site acknowledge timestamp code reserved2' # payload follows. need to fix later: protocol={12 bits protocol, 1 bit addressable, 1 bit tagged, 2 bits reserved}, acknowledge={1 bit acknowledge, 15 bits reserved}
    header_fmt = '<HHI8s6sHQHH'
    header_size = 36
    protocol = 0x3400 # 0x5400

    def __init__(self, packet_type, header_data, payload_data, header_bytes, payload_bytes):
        self.packet_type = packet_type
        self.header_data = header_data
        self.payload_data = payload_data
        self.header_bytes = header_bytes
        self.payload_bytes = payload_bytes

    def __str__(self):
        return(self.packet_type.text + '\n' + str(self.get_data()))

    @classmethod
    def ToBulb(cls, packet_type, site, *payload_data):
        payload_bytes = b""
        if payload_data is not None and packet_type.fmt is not None:
            payload_bytes = pack(packet_type.fmt, *payload_data)

        header_data = (cls.header_size + len(payload_bytes), cls.protocol, 0, bytearray(8), site, 0, 0, packet_type.code, 0)
        header_bytes = pack(cls.header_fmt, *header_data)
        return cls(packet_type, header_data, payload_data, header_bytes, payload_bytes)

    @classmethod
    def FromBulb(cls, byte_data):
        header_bytes = byte_data[:cls.header_size]

        if(len(header_bytes) < cls.header_size):
            raise Exception('Data too short at %d. Must be more than %d.' % (len(header_bytes), cls.header_size))

        PacketData = namedtuple('PacketHeader', cls.header)
        header_data = PacketData._make(unpack(cls.header_fmt, header_bytes))


        payload_bytes = byte_data[cls.header_size:]
        payload_bytes = payload_bytes[:(header_data.size - cls.header_size)]

        if payload_bytes is None or len(byte_data) == cls.header_size:
            payload_bytes = b""

        packet_type = None
        for item in PacketType:
            if item.code == header_data.code:
                packet_type = item
                break

        if packet_type is None:
            raise Exception('No packet type defined.')

        payload_data = None
        if packet_type.fmt is not None:
            if calcsize(packet_type.fmt) is not len(payload_bytes):
                raise Exception('Payload is not the correct length. For packet type %d, length required is %d but got payload length of %d.' % (packet_type.code, calcsize(packet_type.fmt), len(payload_bytes)))

            PacketPayload = namedtuple('PacketPayload', packet_type.payload)
            payload_data = PacketPayload._make(unpack(packet_type.fmt, payload_bytes))

        return cls(packet_type, header_data, payload_data, header_bytes, payload_bytes)

    def get_data(self):
        return self.header_data, self.payload_data

    def get_bytes(self):
        return self.header_bytes + self.payload_bytes
