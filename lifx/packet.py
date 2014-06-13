import sys
from collections import namedtuple
from struct import pack, unpack, calcsize

class PacketTypeDef:

    def __init__(self, text, code, payload, fmt):
        self.text = text
        self.code = code
        self.payload = payload
        self.fmt = fmt

    def __str__(self):
        return("%s Packet - %d" % (self.text, self.code))

class PacketType:

    # Network
    GET_PAN_GATEWAY = PacketTypeDef('Get PAN Gateway', 0x02, None, None) #to bulb
    PAN_GATEWAY = PacketTypeDef('PAN Gateway', 0x03, 'service port', '<bI') #from bulb. note port is little endian

    # Power
    GET_POWER_STATE = PacketTypeDef('Get Power State', 0x14, None, None) #to bulb
    SET_POWER_STATE = PacketTypeDef('Set Power State', 0x15, 'onoff', '<H') #to bulb
    POWER_STATE = PacketTypeDef('Power State', 0x16, 'onoff', '<H') #from bulb

    # Wireless
    GET_WIFI_INFO = PacketTypeDef('Get Wifi Info', 0x10, None, None) # to bulb
    WIFI_INFO = PacketTypeDef('Wifi Info', 0x11, 'signal tx rx mcu_temperature', '<fiih') # from bulb
    GET_WIFI_FIRMWARE_STATE = PacketTypeDef('Get Wifi Firmware State', 0x12, None, None) # to bulb
    WIFI_FIRMWARE_STATE = PacketTypeDef('Wifi Firmware State', 0x13, 'build install version', '<QQI') # from bulb
    GET_WIFI_STATE = PacketTypeDef('Get Wifi State', 0x12d, 'interface', '<b') # to bulb
    SET_WIFI_STATE = PacketTypeDef('Set Wifi State', 0x12e, 'interface wifi_state ip4_address ip6_address', '<bb4b16b') # to bulb
    WIFI_STATE = PacketTypeDef('Wifi State', 0x12f, 'interface wifi_state ip4_address ip6_address', '<bb4b16b') # from bulb
    GET_ACCESS_POINTS = PacketTypeDef('Get Access Points', 0x130, None, None) # to bulb
    SET_ACCESS_POINT = PacketTypeDef('Set Access Points', 0x131, 'interface ssid password security_protocol', '<b32s64sb') # to bulb
    ACCESS_POINT = PacketTypeDef('Accesss Points', 0x132, 'interface ssid security_protocol strength channel', '<b32sbHH') # from bulb

    # Labels and Tags
    GET_BULB_LABEL = PacketTypeDef('Get Bulb Label', 0x17, None, None) #to bulb
    SET_BULB_LABEL = PacketTypeDef('Set Bulb Label', 0x18, 'label', '<32s') #to bulb
    BULB_LABEL = PacketTypeDef('Bulb Label', 0x19, 'label', '<32s') #from bulb
    GET_TAGS = PacketTypeDef('Get Tags', 0x1a, None, None) #to bulb
    SET_TAGS = PacketTypeDef('Set Tags', 0x1b, 'tags', '<Q') #to bulb
    TAGS = PacketTypeDef('Tags', 0x1c, 'tags', 'Q') #from bulb
    GET_TAG_LABELS = PacketTypeDef('Get Tag Labels', 0x1d, 'tags', '<Q') #to bulb
    SET_TAG_LABELS = PacketTypeDef('Set Tag Labels', 0x1e, 'tags label', '<Q32s') #to bulb
    TAG_LABELS = PacketTypeDef('Tag Labels', 0x1f, 'tags label', '<Q32s') #from bulb

    # Colour
    GET_LIGHT_STATE = PacketTypeDef('Get Light State', 0x65, None, None) #to bulb
    SET_LIGHT_COLOUR = PacketTypeDef('Set Light Colour', 0x66, 'stream hue saturation brightness kelvin duration', '<bHHHHI') #to bulb
    SET_WAVEFORM = PacketTypeDef('Set Waveform', 0x67, 'stream transient hue saturation brightness kelvin period cycles duty_cycles waveform', '<b?HHHHIfHb') #to bulb
    SET_DIM_ABSOLUTE = PacketTypeDef('Set Dim Absolute', 0x68, 'brightness duration', '<hI') #to bulb
    SET_DIM_RELATIVE = PacketTypeDef('Set Dim Relative', 0x69, 'brightness duration', '<iI') #to bulb
    #SET_LIGHT_RGBW = PacketTypeDef('Set Light RGBW', 0x, 'red green blue white', '<HHHH') #to bulb
    LIGHT_STATUS = PacketTypeDef('Light Status', 0x6b, 'hue saturation brightness kelvin dim power build_label tags', '<HHHHhH32sQ') #from bulb

    # Time
    GET_TIME = PacketTypeDef('Get Time', 0x04, None, None) #to bulb
    SET_TIME = PacketTypeDef('Set Time', 0x05, 'time', '<Q') #to bulb. note time is little endian
    TIME_STATE = PacketTypeDef('Time State', 0x06, 'time', '<Q') #from bulb. note time is little endian

    #Debug
    GET_RESET_SWITCH = PacketTypeDef('Get Reset Switch', 0x07, None, None) #to bulb
    RESET_SWITCH_STATE = PacketTypeDef('Reset Switch State', 0x08, 'position', '<H') #from bulb
    #GET_DUMMY_LOAD = PacketTypeDef('Get Dummy Load', 0x09, '', '') #to bulb
    #SET_DUMMY_LOAD = PacketTypeDef('Set Dummy Load', 0x0a, '', '') #to bulb
    #DUMMY_LOAD = PacketTypeDef('Dummy Load', 0x0b, '', '') #from bulb
    GET_MESH_INFO = PacketTypeDef('Get Mesh Info', 0x0c, None, None) #to bulb
    MESH_INFO = PacketTypeDef('Mesh Info', 0x0d, 'signal tx rx mcu_temperature', '<fiih') #from bulb. note signal, tx and rx are little endian
    GET_MESH_FIRMWARE = PacketTypeDef('Get Mesh Firmware', 0x0e, None, None) #to bulb
    MESH_FIRMWARE_STATE = PacketTypeDef('Mesh Firmware State', 0x0f, 'build install version', '<QQI') #from bulb
    GET_VERSION = PacketTypeDef('Get Version', 0x20, None, None) #to bulb
    VERSION_STATE = PacketTypeDef('Version State', 0x21, 'vendor product version', '<III') #from bulb
    GET_INFO = PacketTypeDef('Get Info', 0x22, None, None) #to bulb
    INFO = PacketTypeDef('Info', 0x23, 'time uptime downtime', '<QQQ') #from bulb
    GET_MCU_RAIL_VOLTAGE = PacketTypeDef('Get MCU Rail Voltage', 0x24, None, None) #to bulb
    MCU_RAIL_VOLTAGE = PacketTypeDef('MCU Rail Voltage', 0x25, 'voltage', '<I') #from bulb
    REBOOT = PacketTypeDef('Reboot', 0x26, None, None) #to bulb
    SET_FACTORY_TEST_MODE = PacketTypeDef('Set Factory Test Mode', 0x27, 'on', '<b') #to bulb
    DISABLE_FACTORY_TEST_MODE = PacketTypeDef('Disable Factory Test Mode', 0x28, None, None) #to bulb
    #GET_TEMPERATURE = PacketTypeDef('Get Temperature', 0x, None, None) #to bulb
    #TEMPERATURE = PacketTypeDef('Temperature', 0x, 'temperature', '<h') #to bulb

class PacketCode:

    mapper = dict([(getattr(PacketType, attr).code, attr) for attr in dir(PacketType) if not callable(attr) and not attr.startswith("__")])

    @classmethod
    def get_packet_type(class_, code):
        attr = class_.mapper.get(code, None)
        if attr is not None:
            return getattr(PacketType, attr)
        return None

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


        # Some version specfic stuff to handle the fact that python 2 pack takes
        # strings whereas python 3 pack takes bytearrays.
        target_vs = bytearray(8)
        site_vs = site
        if sys.version_info < (3, 0):
            target_vs = str(target_vs)
            site_vs = str(site_vs)

        header_data = (cls.header_size + len(payload_bytes), cls.protocol, 0, target_vs, site_vs, 0, 0, packet_type.code, 0)
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
