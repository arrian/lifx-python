# LIFX Python Library

This project aims to be a simple to use comprehensive python library for interaction with LIFX lightbulbs.

## Usage

 ```python

import time
import lifx

# Print a LIFX packet
def print_packet(packet):
    print()
    if packet is not None:
        print(packet.packet_type.text)
        print(packet.get_data())
    else:
        print("Packet could not be parsed.")



# Create the LIFX connection
network = lifx.Network()

# Listen to all LIFX packets, printing the packet when received
network.listen(print_packet)

# Turn on the LIFX bulb
network.send(lifx.PacketType.SET_POWER_STATE, lifx.Power.ON)

# Set the colour of the bulb
network.send(lifx.PacketType.SET_LIGHT_COLOUR, 0, 30000, 30000, 30000, 1000, 0)

# Request bulb state
network.send(lifx.PacketType.GET_LIGHT_STATE)

# keep listen running
while(True): 
    time.sleep(1)

thread.join()

 ```