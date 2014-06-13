from time import sleep
import lifx

# Create the LIFX connection
lights = lifx.Lifx()

# Turn on the lights
lights.on()

# Set all the lights to green
lights.set_colour(lifx.Colour.GREEN)

# You can also be more specific with your colour settings: hue, saturation, brightness, kelvin, transition_duration
lights.set_colour(0, 10000, 10000, 1000, 5000)

# Get the lights' colours
print(lights.get_colours())

# Get the lights' labels
print(lights.get_labels())

# Get the lights' internal time
print(lights.get_time())

# Get the wifi information
print(lights.get_wifi_info())

# Get the available access points
print(lights.get_access_points())

# Asynchronous print all LIFX network packets and continue.
# Pass any function here that takes a one packet type argument.
lights.monitor(lights.print_packet)

while True:
	sleep(1)
