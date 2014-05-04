import socket
import struct
from time import time, sleep
import select
from threading import Thread

from lifx.packet import Packet
from lifx.packet_type import PacketType


class Network:
    connection = None
    port = 56700
    broadcast = '255.255.255.255'
    ip = '0.0.0.0'
    site = bytearray(6)

    def __init(self):
        self.connect()

    def check_connection(self):
        if self.connection is None:
            self.connect()
        if self.connection is None:
            raise Exception('Failed to connect.')

    def connect(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind((self.ip, self.port))

        p = Packet.ToBulb(PacketType.GET_PAN_GATEWAY, self.site, None)
        udp_socket.sendto(bytes(p.get_bytes()), (self.broadcast, self.port))
        
        for x in range(5):
            try:
                udp_socket.settimeout(1)
                data, address = udp_socket.recvfrom(2048)
                packet = Packet.FromBulb(data)
                if packet is not None:
                    header,payload = packet.get_data()

                    if header.code is PacketType.PAN_GATEWAY.code:
                        break
            except socket.timeout:
                pass
        udp_socket.close()
        if header.code is not PacketType.PAN_GATEWAY.code:
            connection = None
            return

        print('Found light at %s' % (address[0],))

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(2.0)
        tcp_socket.connect(address)
        tcp_socket.setblocking(0)
        self.site = header.site
        self.connection = tcp_socket

    def send(self, packet_type, *data):
        self.check_connection()
        self.connection.sendall(Packet.ToBulb(packet_type, self.site, *data).get_bytes())

    def receive(self):
        self.check_connection()
        ready = select.select([self.connection], [], [], 2)
        if ready[0]:
            data = self.connection.recv(2048)
            return Packet.FromBulb(data)
        return None

    # async method to list to packets. recv_func is called when packet received.
    def listen(self, recv_func):
        self.check_connection()

        def perform_recv(val):
            while(True):
                packet = self.receive()
                recv_func(packet)

        thread = Thread(target = perform_recv, args = (10, ))
        thread.start()
