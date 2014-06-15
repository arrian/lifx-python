from lifx.simulator import Simulator

# This simulates the behaviour of a LIFX lightbulb locally.

simulator = Simulator(bulb_label = b'Example Bulb')
simulator.start()