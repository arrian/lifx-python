from enum import Enum

class PacketType(Enum):

    def __init__(self, text, code, payload, fmt):
        self.text = text
        self.code = code
        self.payload = payload
        self.fmt = fmt

    # Network
    GET_PAN_GATEWAY = ('Get PAN Gateway', 0x02, None, None) #to bulb
    PAN_GATEWAY = ('PAN Gateway', 0x03, 'service port', '<bI') #from bulb. note port is little endian

    # Power
    GET_POWER_STATE = ('Get Power State', 0x14, None, None) #to bulb
    SET_POWER_STATE = ('Set Power State', 0x15, 'onoff', '<H') #to bulb
    POWER_STATE = ('Power State', 0x16, 'onoff', '<H') #from bulb

    # Wireless
    GET_WIFI_INFO = ('Get Wifi Info', 0x10, None, None) # to bulb
    WIFI_INFO = ('Wifi Info', 0x11, 'signal tx rx mcu_temperature', '<fiih') # from bulb
    GET_WIFI_FIRMWARE_STATE = ('Get Wifi Firmware State', 0x12, None, None) # to bulb
    WIFI_FIRMWARE_STATE = ('Wifi Firmware State', 0x13, 'build install version', '<QQI') # from bulb
    GET_WIFI_STATE = ('Get Wifi State', 0x12d, 'interface', '<b') # to bulb
    SET_WIFI_STATE = ('Set Wifi State', 0x12e, 'interface wifi_state ip4_address ip6_address', '<bb4b16b') # to bulb
    WIFI_STATE = ('Wifi State', 0x12f, 'interface wifi_state ip4_address ip6_address', '<bb4b16b') # from bulb
    GET_ACCESS_POINTS = ('Get Access Points', 0x130, None, None) # to bulb
    SET_ACCESS_POINT = ('Set Access Points', 0x131, 'interface ssid password security_protocol', '<b32s64sb') # to bulb
    ACCESS_POINT = ('Accesss Points', 0x132, 'interface ssid security_protocol strength channel', '<b32sbHH') # from bulb

    # Labels
    GET_BULB_LABEL = ('Get Bulb Label', 0x17, None, None) #to bulb
    SET_BULB_LABEL = ('Set Bulb Label', 0x18, 'label', '<32s') #to bulb
    BULB_LABEL = ('Bulb Label', 0x19, 'label', '<32s') #from bulb

    # Tags
    GET_TAGS = ('Get Tags', 0x1a, None, None) #to bulb
    SET_TAGS = ('Set Tags', 0x1b, 'tags', '<Q') #to bulb
    TAGS = ('Tags', 0x1c, 'tags', 'Q') #from bulb
    GET_TAG_LABELS = ('Get Tag Labels', 0x1d, 'tags', '<Q') #to bulb
    SET_TAG_LABELS = ('Set Tag Labels', 0x1e, 'tags label', '<Q32s') #to bulb
    TAG_LABELS = ('Tag Labels', 0x1f, 'tags label', '<Q32s') #from bulb

    # Colour
    GET_LIGHT_STATE = ('Get Light State', 0x65, None, None) #to bulb
    SET_LIGHT_COLOUR = ('Set Light Colour', 0x66, 'stream hue saturation brightness kelvin duration', '<bHHHHI') #to bulb
    SET_WAVEFORM = ('Set Waveform', 0x67, 'stream transient hue saturation brightness kelvin period cycles duty_cycles waveform', '<b?HHHHIfHb') #to bulb
    SET_DIM_ABSOLUTE = ('Set Dim Absolute', 0x68, 'brightness duration', '<hI') #to bulb
    SET_DIM_RELATIVE = ('Set Dim Relative', 0x69, 'brightness duration', '<iI') #to bulb
    #SET_LIGHT_RGBW = ('Set Light RGBW', 0x, 'red green blue white', '<HHHH') #to bulb
    LIGHT_STATUS = ('Light Status', 0x6b, 'hue saturation brightness kelvin dim power build_label tags', '<HHHHhH32sQ') #from bulb

    # Time
    GET_TIME = ('Get Time', 0x04, None, None) #to bulb
    SET_TIME = ('Set Time', 0x05, 'time', '<Q') #to bulb. note time is little endian
    TIME_STATE = ('Time State', 0x06, 'time', '<Q') #from bulb. note time is little endian

    #Debug
    GET_RESET_SWITCH = ('Get Reset Switch', 0x07, None, None) #to bulb
    RESET_SWITCH_STATE = ('Reset Switch State', 0x08, 'position', '<H') #from bulb
    #GET_DUMMY_LOAD = ('Get Dummy Load', 0x09, '', '') #to bulb
    #SET_DUMMY_LOAD = ('Set Dummy Load', 0x0a, '', '') #to bulb
    #DUMMY_LOAD = ('Dummy Load', 0x0b, '', '') #from bulb
    GET_MESH_INFO = ('Get Mesh Info', 0x0c, None, None) #to bulb
    MESH_INFO = ('Mesh Info', 0x0d, 'signal tx rx mcu_temperature', 'fiih') #from bulb. note signal, tx and rx are little endian
    GET_MESH_FIRMWARE = ('Get Mesh Firmware', 0x0e, None, None) #to bulb
    MESH_FIRMWARE_STATE = ('Mesh Firmware State', 0x0f, 'build install version', '<QQI') #from bulb
    GET_VERSION = ('Get Version', 0x20, None, None) #to bulb
    VERSION_STATE = ('Version State', 0x21, 'vendor product version', '<III') #from bulb
    GET_INFO = ('Get Info', 0x22, None, None) #to bulb
    INFO = ('Info', 0x23, 'time uptime downtime', '<QQQ') #from bulb
    GET_MCU_RAIL_VOLTAGE = ('Get MCU Rail Voltage', 0x24, None, None) #to bulb
    MCU_RAIL_VOLTAGE = ('MCU Rail Voltage', 0x25, 'voltage', '<I') #from bulb
    REBOOT = ('Reboot', 0x26, None, None) #to bulb
    SET_FACTORY_TEST_MODE = ('Set Factory Test Mode', 0x27, 'on', 'b') #to bulb
    DISABLE_FACTORY_TEST_MODE = ('Disable Factory Test Mode', 0x28, None, None) #to bulb
    #GET_TEMPERATURE = ('Get Temperature', 0x, None, None) #to bulb
    #TEMPERATURE = ('Temperature', 0x, 'temperature', '<h') #to bulb

