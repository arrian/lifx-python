from time import sleep
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

# Asynchronous print all LIFX network packets and continue. 
# Pass any function here that takes a one packet type argument.
client.monitor(lambda packet: print('Packet could not be parsed.\n') if packet is None else print(str(packet) + '\n'))

while True:
	sleep(1)
