from time import sleep
import lifx

lights = lifx.Lifx()
lights.on()

while(True):
	lights.set_colour(lifx.Colour.GREEN, 40000, 5000, 1000, 2000)
	sleep(2)
	lights.set_colour(lifx.Colour.GREEN, 40000, 500, 1000, 2000)
	sleep(3)

