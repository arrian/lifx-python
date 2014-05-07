from time import sleep
import random
import lifx

lights = lifx.Lifx()
lights.on()

while True:
	lights.set_colour(random.randint(7000, 7500), 40000, random.randint(2200, 3000), 1000, random.randint(80, 180))
	sleep(random.random() / 2)

