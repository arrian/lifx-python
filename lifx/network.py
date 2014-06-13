import socket
import struct
from time import time, sleep
import select
from threading import Thread

from .packet import *


class Network:
    connection = None
    port = 56700
    broadcast = '255.255.255.255'
    ip = '0.0.0.0'
    site = bytearray(6)
    receive_size = 2048
    timeout = 1

    def __init(self):
        self.connect()

    def check_connection(self):
        if self.connection is None:
            self.connect()
        if self.connection is None:
            raise Exception('Failed to connect.')

    def connect(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp.bind((self.ip, self.port))

        p = Packet.ToBulb(PacketType.GET_PAN_GATEWAY, self.site, None)
        udp.sendto(bytes(p.get_bytes()), (self.broadcast, self.port))
        
        for x in range(10):
            try:
                udp.settimeout(self.timeout)
                data, address = udp.recvfrom(self.receive_size)
                packet = Packet.FromBulb(data)
                if packet is not None:
                    header,payload = packet.get_data()

                    if header.code is PacketType.PAN_GATEWAY.code:
                        break
            except socket.timeout:
                raise Exception('Handshake timed out.')
        udp.close()
        udp = None
        if header.code is not PacketType.PAN_GATEWAY.code:
            connection = None
            return

        print('Found light at %s' % (address[0],))

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.settimeout(self.timeout)
        tcp.connect(address)
        tcp.setblocking(0)
        self.site = header.site
        self.connection = tcp

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def send(self, packet_type, *data):
        self.check_connection()
        self.connection.sendall(Packet.ToBulb(packet_type, self.site, *data).get_bytes())

    def receive(self):
        self.check_connection()
        ready = select.select([self.connection], [], [], 2)
        if ready[0]:
            data = self.connection.recv(self.receive_size)
            return Packet.FromBulb(data)
        return None

    # asynchronous method to call recv_func whenever a packet is received.
    def listen_async(self, recv_func, packet_filter = None, max_packets = None):
        self.check_connection()

        def perform_recv(val):
            packet_count = 0
            while max_packets is None or packet_count < max_packets:
                packet = self.receive()
                if packet is not None and (packet_filter is None or packet_filter.code is packet.packet_type.code):
                    recv_func(packet)
                packet_count += 1

        thread = Thread(target = perform_recv, args = (10, ))
        thread.start()

    # synchronous method to get the first of the specified packets
    def listen_sync(self, packet_filter, max_packets = None):
        self.check_connection()

        packet_count = 0
        while max_packets is None or packet_count < max_packets:
            packet = self.receive()
            if packet is not None and packet.packet_type.code is packet_filter.code:
                return packet
            packet_count += 1
        return None



