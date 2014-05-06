
class Service:
    UDP = 1
    TCP = 2

class ResetSwitchPosition:
    UP = 0
    DOWN = 1

class Interface:
    SOFT_AP = 1
    STATION = 2

class WifiStatus:
    CONNECTING = 0
    CONNECTED = 1
    FAILED = 2
    OFF = 3

class SecurityProtocol:
    OPEN = 1
    WEP_PSK = 2
    WPA_TKIP_PSK = 3
    WPA_AES_PSK = 4
    WPA2_AES_PSK = 5
    WPA2_TKIP_PSK = 6
    WPA2_MIXED_PSK = 7      

class Power:
    OFF = 0
    ON = 0xffff

class Waveform:
    SAW = 0
    SINE = 1
    HALF_SINE = 2
    TRIANGLE = 3
    PULSE = 4

class Colour:
    RED = 0
    ORANGE = 5000
    YELLOW = 8000
    GREEN = 18000
    BLUE = 42720

class Brightness:
    OFF = 0
    DIM = 1000
    MOOD = 2500
    NORMAL = 6000
    FULL = 65000


