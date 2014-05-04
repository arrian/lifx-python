from time import sleep
import lifx

client = lifx.Lifx()
client.set_power_state(lifx.Power.ON)

while(True):
	client.set_light_colour(30000, 40000, 5000, 1000, 2000)
	sleep(2)
	client.set_light_colour(30000, 40000, 500, 1000, 2000)
	sleep(3)

