import sys
from collections import namedtuple
from struct import pack, unpack, calcsize

class PacketDirection:
    FROM_BULB, TO_BULB = range(2)

class PacketTypeDef(object):

    def __init__(self, text, code, payload, fmt, direction):
        self.text = text
        self.code = code
        self.payload = payload
        self.fmt = fmt
        self.direction = direction

    def __str__(self):
        return("%s Packet - %d" % (self.text, self.code))

class PacketTypeDefFromBulb(PacketTypeDef):
    def __init__(self, text, code, payload, fmt):
        super(PacketTypeDefFromBulb, self).__init__(text, code, payload, fmt, PacketDirection.FROM_BULB)

class PacketTypeDefToBulb(PacketTypeDef):
    def __init__(self, text, code, payload, fmt):
        super(PacketTypeDefToBulb, self).__init__(text, code, payload, fmt, PacketDirection.TO_BULB)

class PacketType:

    # Network
    GET_PAN_GATEWAY = PacketTypeDefToBulb('Get PAN Gateway', 0x02, None, None)
    PAN_GATEWAY = PacketTypeDefFromBulb('PAN Gateway', 0x03, 'service port', '<bI') # note port is little endian

    # Power
    GET_POWER_STATE = PacketTypeDefToBulb('Get Power State', 0x14, None, None)
    SET_POWER_STATE = PacketTypeDefToBulb('Set Power State', 0x15, 'onoff', '<H')
    POWER_STATE = PacketTypeDefFromBulb('Power State', 0x16, 'onoff', '<H')

    # Wireless
    GET_WIFI_INFO = PacketTypeDefToBulb('Get Wifi Info', 0x10, None, None)
    WIFI_INFO = PacketTypeDefFromBulb('Wifi Info', 0x11, 'signal tx rx mcu_temperature', '<fiih')
    GET_WIFI_FIRMWARE_STATE = PacketTypeDefToBulb('Get Wifi Firmware State', 0x12, None, None)
    WIFI_FIRMWARE_STATE = PacketTypeDefFromBulb('Wifi Firmware State', 0x13, 'build install version', '<QQI')
    GET_WIFI_STATE = PacketTypeDefToBulb('Get Wifi State', 0x12d, 'interface', '<b')
    SET_WIFI_STATE = PacketTypeDefToBulb('Set Wifi State', 0x12e, 'interface wifi_state ip4_address ip6_address', '<bb4b16b')
    WIFI_STATE = PacketTypeDefFromBulb('Wifi State', 0x12f, 'interface wifi_state ip4_address ip6_address', '<bb4b16b')
    GET_ACCESS_POINTS = PacketTypeDefToBulb('Get Access Points', 0x130, None, None)
    SET_ACCESS_POINT = PacketTypeDefToBulb('Set Access Points', 0x131, 'interface ssid password security_protocol', '<b32s64sb')
    ACCESS_POINT = PacketTypeDefFromBulb('Accesss Points', 0x132, 'interface ssid security_protocol strength channel', '<b32sbHH')

    # Labels and Tags
    GET_BULB_LABEL = PacketTypeDefToBulb('Get Bulb Label', 0x17, None, None)
    SET_BULB_LABEL = PacketTypeDefToBulb('Set Bulb Label', 0x18, 'label', '<32s')
    BULB_LABEL = PacketTypeDefFromBulb('Bulb Label', 0x19, 'label', '<32s')
    GET_TAGS = PacketTypeDefToBulb('Get Tags', 0x1a, None, None)
    SET_TAGS = PacketTypeDefToBulb('Set Tags', 0x1b, 'tags', '<Q')
    TAGS = PacketTypeDefFromBulb('Tags', 0x1c, 'tags', 'Q')
    GET_TAG_LABELS = PacketTypeDefToBulb('Get Tag Labels', 0x1d, 'tags', '<Q')
    SET_TAG_LABELS = PacketTypeDefToBulb('Set Tag Labels', 0x1e, 'tags label', '<Q32s')
    TAG_LABELS = PacketTypeDefFromBulb('Tag Labels', 0x1f, 'tags label', '<Q32s')

    # Colour
    GET_LIGHT_STATE = PacketTypeDefToBulb('Get Light State', 0x65, None, None)
    SET_LIGHT_COLOUR = PacketTypeDefToBulb('Set Light Colour', 0x66, 'stream hue saturation brightness kelvin duration', '<bHHHHI')
    SET_WAVEFORM = PacketTypeDefToBulb('Set Waveform', 0x67, 'stream transient hue saturation brightness kelvin period cycles duty_cycles waveform', '<b?HHHHIfHb')
    SET_DIM_ABSOLUTE = PacketTypeDefToBulb('Set Dim Absolute', 0x68, 'brightness duration', '<hI')
    SET_DIM_RELATIVE = PacketTypeDefToBulb('Set Dim Relative', 0x69, 'brightness duration', '<iI')
    #SET_LIGHT_RGBW = PacketTypeDefToBulb('Set Light RGBW', 0x, 'red green blue white', '<HHHH')
    LIGHT_STATUS = PacketTypeDefFromBulb('Light Status', 0x6b, 'hue saturation brightness kelvin dim power build_label tags', '<HHHHhH32sQ')

    # Time
    GET_TIME = PacketTypeDefToBulb('Get Time', 0x04, None, None)
    SET_TIME = PacketTypeDefToBulb('Set Time', 0x05, 'time', '<Q') # note time is little endian
    TIME_STATE = PacketTypeDefFromBulb('Time State', 0x06, 'time', '<Q') # note time is little endian

    #Debug
    GET_RESET_SWITCH = PacketTypeDefToBulb('Get Reset Switch', 0x07, None, None)
    RESET_SWITCH_STATE = PacketTypeDefFromBulb('Reset Switch State', 0x08, 'position', '<H')
    #GET_DUMMY_LOAD = PacketTypeDefToBulb('Get Dummy Load', 0x09, '', '')
    #SET_DUMMY_LOAD = PacketTypeDefToBulb('Set Dummy Load', 0x0a, '', '')
    #DUMMY_LOAD = PacketTypeDefFromBulb('Dummy Load', 0x0b, '', '')
    GET_MESH_INFO = PacketTypeDefToBulb('Get Mesh Info', 0x0c, None, None)
    MESH_INFO = PacketTypeDefFromBulb('Mesh Info', 0x0d, 'signal tx rx mcu_temperature', '<fiih') # note signal, tx and rx are little endian
    GET_MESH_FIRMWARE = PacketTypeDefToBulb('Get Mesh Firmware', 0x0e, None, None)
    MESH_FIRMWARE_STATE = PacketTypeDefFromBulb('Mesh Firmware State', 0x0f, 'build install version', '<QQI')
    GET_VERSION = PacketTypeDefToBulb('Get Version', 0x20, None, None)
    VERSION_STATE = PacketTypeDefFromBulb('Version State', 0x21, 'vendor product version', '<III')
    GET_INFO = PacketTypeDefToBulb('Get Info', 0x22, None, None)
    INFO = PacketTypeDefFromBulb('Info', 0x23, 'time uptime downtime', '<QQQ')
    GET_MCU_RAIL_VOLTAGE = PacketTypeDefToBulb('Get MCU Rail Voltage', 0x24, None, None)
    MCU_RAIL_VOLTAGE = PacketTypeDefFromBulb('MCU Rail Voltage', 0x25, 'voltage', '<I')
    REBOOT = PacketTypeDefToBulb('Reboot', 0x26, None, None)
    SET_FACTORY_TEST_MODE = PacketTypeDefToBulb('Set Factory Test Mode', 0x27, 'on', '<b')
    DISABLE_FACTORY_TEST_MODE = PacketTypeDefToBulb('Disable Factory Test Mode', 0x28, None, None)
    #GET_TEMPERATURE = PacketTypeDefToBulb('Get Temperature', 0x, None, None)
    #TEMPERATURE = PacketTypeDefToBulb('Temperature', 0x, 'temperature', '<h')

class PacketCode:

    mapper = dict([(getattr(PacketType, attr).code, attr) for attr in dir(PacketType) if not callable(attr) and not attr.startswith("__")])

    @classmethod
    def get_packet_type(class_, code):
        attr = class_.mapper.get(code, None)
        if attr is not None:
            return getattr(PacketType, attr)
        return None

class Packet:

    # payload follows. need to fix later: protocol={12 bits protocol, 
    # 1 bit addressable, 1 bit tagged, 2 bits reserved}, acknowledge
    # ={1 bit acknowledge, 15 bits reserved}
    header = 'size protocol reserved1 target reserved2 site acknowledge timestamp code reserved3' 
    
    header_fmt = '<HHI6sH6sHQHH'
    header_size = 36
    protocol = 0x3400 # 0x5400 = bulb protocol
    protocol_bulb = 0x5400

    def __init__(self, packet_type, header_data, payload_data, header_bytes, payload_bytes):
        self.packet_type = packet_type
        self.header_data = header_data
        self.payload_data = payload_data
        self.header_bytes = header_bytes
        self.payload_bytes = payload_bytes

    def __str__(self):
        return(self.packet_type.text + '\n' + str(self.get_data()))

    @classmethod
    def AsBulb(cls, packet_type, address, site, *payload_data):
        packet = Packet.ToBulb(packet_type, address, site, *payload_data)
        packet.protocol = packet.protocol_bulb # the bulb uses a different protocol value
        return packet

    @classmethod
    def ToBulb(cls, packet_type, target, site, *payload_data):
        payload_bytes = b""
        if payload_data is not None and packet_type.fmt is not None:
            payload_bytes = pack(packet_type.fmt, *payload_data)


        # Some version specfic stuff to handle the fact that python 2 pack takes
        # strings whereas python 3 pack takes bytearrays.
        target_vs = target
        site_vs = site
        if sys.version_info < (3, 0):
            target_vs = str(target_vs)
            site_vs = str(site_vs)

        header_data = (cls.header_size + len(payload_bytes), cls.protocol, 0, target_vs, 0, site_vs, 0, 0, packet_type.code, 0)
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

        packet_type = PacketCode.get_packet_type(header_data.code)
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
