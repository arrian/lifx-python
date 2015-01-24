import socket
import struct
from time import time, sleep
import select
from threading import Thread

from .packet import *

# handle tcp not supported
import errno
from socket import error as socket_error


class Network:
    connection = None
    port = 56700
    ip = '0.0.0.0'
    broadcast_ip = '255.255.255.255'
    target = bytearray(6)
    site = bytearray(6)
    receive_size = 2048
    timeout = 2
    address = None

    def __init__(self, connect = True):
        if connect:
            self.connect()

    def to_mac(self, addr):
        return ':'.join('%02x' % b for b in addr)

    def check_connection(self):
        if self.connection is None:
            self.connect()
        if self.connection is None:
            raise Exception('Failed to connect.')

    def connect(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp.bind((self.ip, self.port))
        print(udp.getsockname())

        p = Packet.ToBulb(PacketType.GET_PAN_GATEWAY, self.target, self.site, None)
        udp.sendto(bytes(p.get_bytes()), (self.broadcast_ip, self.port))
        
        for x in range(10):
            try:
                udp.settimeout(self.timeout)
                data, self.address = udp.recvfrom(self.receive_size)
                packet = Packet.FromBulb(data)
                if packet is not None:
                    header,payload = packet.get_data()
                    if header.code is PacketType.PAN_GATEWAY.code:
                        break
            except socket.timeout:
                raise Exception('Handshake timed out.')

        if header.code is not PacketType.PAN_GATEWAY.code:
            connection = None
            raise Exception('Connection failed. Could not determine the gateway.')

        print('Found light at %s:%s' % (self.address[0],self.address[1]))

        self.site = header.site
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(self.timeout)
            tcp.connect(self.address)
            tcp.setblocking(0)
            self.connection = tcp
            print('Using tcp')
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                raise serr
            self.connection = udp # latest versions of firmware >= 1.2 do not support tcp? fall back to udp
            print('Using udp')

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def send(self, packet_type, *data):
        self.check_connection()
        packet = Packet.ToBulb(packet_type, self.target, self.site, *data).get_bytes()

        if self.connection.type is socket.SOCK_DGRAM:
            self.connection.sendto(packet, self.address)
        else:
            self.connection.sendall(packet)

    def receive(self, timeout = 1):
        self.check_connection()
        ready = select.select([self.connection], [], [], timeout)
        if ready[0]:
            data = self.connection.recv(self.receive_size)
            return Packet.FromBulb(data)
        return None

    def broadcast(self, packet):
        broadcast_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_connection.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_connection.bind((self.ip, 0))
        broadcast_connection.sendto(bytes(packet.get_bytes()), (self.broadcast_ip, self.port))
        broadcast_connection.close()

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

    # Synchronous method to get the first of the specified packets.
    # Packet filter is a single packet code or a list of packet codes.
    def listen_sync(self, packet_filter, num_packets = 1, timeout = 2):
        self.check_connection()
        start_time = time()

        packets = []

        while True:
            packet = self.receive()
            if packet is not None and (packet.packet_type.code is packet_filter.code or (isinstance(packet_filter, list) and packet.packet_type.code in packet_filter)):
                if num_packets == 1:
                    return packet
                else:
                    packets.append(packet)

            if timeout is not None and time() > start_time + timeout:
                break
        if num_packets == 1:
            return None
        return packets



