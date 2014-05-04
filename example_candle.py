from time import sleep
import random
import lifx

client = lifx.Lifx()
client.set_power_state(lifx.Power.ON)

while True:
	client.set_light_colour(random.randint(6000, 6500), 40000, random.randint(2200, 3000), 1000, random.randint(80, 180))
	sleep(random.random() / 2)

