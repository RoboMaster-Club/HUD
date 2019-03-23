#!/usr/bin/env python
import pygame
import serial
from serial.threaded import ReaderThread
from queue import LifoQueue, Full, Empty
import os
import sys
import platform
from util import *

# Initialization
system = platform.system()
if system != 'Darwin':
	drivers = ['fbcon', 'directfb', 'svgalib']
	found = False
	for driver in drivers:
		# Make sure that SDL_VIDEODRIVER is set
		if not os.getenv('SDL_VIDEODRIVER'):
			os.putenv('SDL_VIDEODRIVER', driver)
		try:
			pygame.display.init()
		except pygame.error:
			print('Driver: %s failed.' % driver)
			continue
		found = True
		break

	if not found:
		raise Exception('No suitable video driver found!')

pygame.display.init()
pygame.font.init()

# Text
textfont = pygame.font.Font('./resource/fonts/RobotSlab/RobotoSlab-Thin.ttf', 15)
textFormatter = TextFormatter(textfont, WHITE)

# Serial Configuration
ser = serial.Serial()
ser.port = '/dev/cu.usbserial-00000000' if system == 'Darwin' else '/dev/ttyAMA0'
ser.baudrate = 115200
ser.parity = serial.PARITY_EVEN
ser.open()

# Start serial data thread
serialThread = ReaderThread(ser, ReadData)
serialThread.start()

# Start screen
displayMode = not pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE if system == 'Darwin' else pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(RESOLUTION, displayMode)

running = True
clock = pygame.time.Clock()

while running:
	# Run loop at most FRAME_RATE per seconds
	clock.tick(FRAME_RATE)

	#--------------------------------
	# Event handling
	#--------------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == 27:
				running = False

	#--------------------------------
	# Serial data reading (blocking)
	#--------------------------------
	# TODO Use C struct
	data = bufferQueue.get()
	data = data.strip()
	data = data.split(delimiter)
	n = len(data)
	data = [(data[i], data[i + 1]) for i in range(0, n, 2)]
	data = dict(data)
	capVolt = eval(data.pop('capVolt'))


	#--------------------------------
	# Super Capacitor Booster Display
	#--------------------------------

	# Create new strip
	# -1 * height as the coordinate system is inverted
	boostStrip = pygame.Rect(BOOSTSTRIP_LEFT, BOOSTSTRIP_TOP,
							BOOSTSTRIP_WIDTH, -capVolt * BOOSTSTRIP_HEIGHT // MaxCapVolt)

	#--------------------------------
	# Text Display
	#--------------------------------

	# Text info display
	sensorData = "FPS: %.2f\n" % clock.get_fps()
	for key in data.keys():
		sensorData += "%s: %s\n" % (key, data[key])

	# Text renderers
	# Align to the strip
	textSurfaces = textFormatter.format(sensorData,
										(WIDTH - SCREEN_MARGIN - BOOSTSTRIP_WIDTH - 10,
										(HEIGHT - BOOSTSTRIP_HEIGHT) // 2))

	#--------------------------------
	# Screen Update
	#--------------------------------

	screen.fill(BLACK)

	# Text update
	for surface, pos in textSurfaces:
		screen.blit(surface, pos)

	# Boost strip update
	pygame.draw.rect(screen, BOOSTSTRIP_FRAME_COLOR, BOOSTSTRIP_FRAME, BOOSTSTRIP_FRAME_WIDTH)  # Draw Frame
	pygame.draw.rect(screen, BOOSTSTRIP_COLOR, boostStrip, 0)  # Draw actual boost strip

	# Flip the whole screen
	flipped = pygame.transform.flip(screen, False, True)
	# screen.blit(flipped, (0, 0))
	pygame.display.update()
serialThread.close()
pygame.quit()
