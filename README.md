# LIFX Python Library

This project aims to be a simple to use comprehensive python library for interaction with LIFX lightbulbs.

## Usage

 ```python

import time
import lifx

# Create the LIFX client
client = lifx.Lifx()

# Turn on the LIFX bulbs
client.on()

# Set the LIFX bulb colour: hue, saturation, brightness, kelvin, transition_duration
client.set_light_colour(lifx.Colour.GREEN, 30000, 30000, 1000, 5000)

# Get the LIFX bulb colour
print(client.get_light_colour())

# Get the LIFX bulb label
print(client.get_bulb_label())

# Get the bulb internal time
print(client.get_time())

# Show wifi information
print(client.get_wifi_info())

# Show one available access point
print(client.get_access_points())


# Asynchronous print all LIFX network packets and continue
client.monitor(print)

thread.join()

 ```