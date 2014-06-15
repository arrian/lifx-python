from .packet import *
from .network import Network
import string
import random
import threading
import os

try:
    import queue
except ImportError:
    import Queue as queue # backwards compatibility for Python 2

class Simulator:
    """ 
    Simulates a LIFX bulb locally.
    """
    network = None
    broadcast_queue = queue.Queue()

    def __init__(self, network = None, listen_port = 56700, mac_address = b'\xd0s\xd5\x00\xd4\xc3', hue = 0, saturation = 10000, brightness = 10000, kelvin = 1000, dim = 0, power = 1, wifi_info = (1.0, 0, 0, 10), wifi_firmware_state = (0, 0, 0), access_point = (0, b'Dummy Network', 0, 10, 10), bulb_label = b'LIFX Bulb Emulator #' + os.urandom(4), bulb_tags = [b'dummy1', b'dummy2']):
        self.network = network
        self.listen_port = listen_port
        self.mac_address = mac_address
        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness
        self.kelvin = kelvin
        self.dim = dim
        self.power = power
        self.wifi_info = wifi_info
        self.wifi_firmware_state = wifi_firmware_state
        self.access_point = access_point
        self.bulb_label = bulb_label
        self.bulb_tags = bulb_tags

        if self.network is None:
            self.network = Network(False)

    def start(self):
        self.broadcast_pan()
        self.broadcast_status()
        self.broadcast_firmware_state()
        self.listen()

    def broadcast_pan(self):
        print('Broadcasting PAN update.')
        self.broadcast_queue.put(Packet.AsBulb(PacketType.PAN_GATEWAY, self.mac_address, self.mac_address, 1, self.listen_port))
        threading.Timer(10, self.broadcast_pan).start()

    def broadcast_status(self):
        print('Broadcasting light status update.')
        self.broadcast_queue.put(Packet.AsBulb(PacketType.LIGHT_STATUS, self.mac_address, self.mac_address, self.hue, self.saturation, self.brightness, self.kelvin, self.dim, self.power, self.bulb_label, len(self.bulb_tags)))
        threading.Timer(20, self.broadcast_status).start()

    def broadcast_firmware_state(self):
        print('Broadcasting mesh firmware state update.')

        threading.Timer(20, self.broadcast_firmware_state).start()

    #listens and responds to requests
    def listen(self):
        while True:
            while not self.broadcast_queue.empty():
                packet = self.broadcast_queue.get()
                print(str(packet))
                self.network.broadcast(packet)
            self.network.listen_sync(PacketType.GET_PAN_GATEWAY, 1, 1)

    def get_time(self):
        int(round(time.time()))



