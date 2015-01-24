# This example demonstrates setting the bulb colour to sampled pixels from an image.
# Pillow (https://github.com/python-pillow/Pillow) or PIL is required to load images.
from PIL import Image

import lifx
import colorsys
from time import sleep

# Connect to the bulb and ensure it is on
lights = lifx.Lifx()
lights.on()

# Load the image
im = Image.open('kelvin.png')
pix = im.load()

# Loop through the pixels
for i in range(0,im.size[1]):
	for j in range(0,im.size[0]):
		rgb = pix[j,i]
		hsv = colorsys.rgb_to_hsv(rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0)

		lights.set_colour(hsv[0] * 60000, hsv[1] * 60000, hsv[2] * 60000, 1000, 200)

		print('rgb' + str(rgb))

		sleep(0.02)

