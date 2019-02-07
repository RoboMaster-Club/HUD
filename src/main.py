#!/usr/bin/env python
import pygame

# Initialization
pygame.init()

# Constants Definitioin
RESOLUTION = WIDTH, HEIGHT = (480, 320)
FRAME_RATE = 30

# Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screen = pygame.display.set_mode(RESOLUTION)
running = True
clock = pygame.time.Clock()

capVolt = 0

while running:
	# Run loop at most FRAME_RATE per seconds
	clock.tick(FRAME_RATE)

	# Get events
	for event in pygame.event.get():
		# only do something if the event is of type QUIT
		if event.type == pygame.QUIT:
			# change the value to False, to exit the main loop
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.unicode == "a" or event.unicode == "A":
				# Add capacitor voltage
				capVolt += 1
			elif event.unicode == "d" or event.unicode == "D":
				# Decrease capacitor voltage
				capVolt -= 1

	# Correct value
	capVolt = 10 if capVolt > 10 else capVolt
	capVolt = 0 if capVolt < 0 else capVolt

	# Text info display
	fps = clock.get_fps()
	time = clock.get_rawtime()
	formatStr = "FPS: %.2f | Time: %.2f" % (fps, time / 1000)
	capDisplay = "[%-10s]" % (capVolt * "#")

	# Text renderers
	textfont = pygame.font.Font('./fonts/CursedTimerULiL.ttf', 20)
	boostfont = pygame.font.Font('./fonts/CursedTimerULiL.ttf', 20)

	# Render
	textsurface = textfont.render(formatStr, False, WHITE)
	boostStrip = boostfont.render(capDisplay, False, WHITE)

	# Update screen		
	screen.fill(BLACK)
	textPos = textfont.size(formatStr)[0]  # Get the width of string in pixels
	screen.blit(textsurface, (WIDTH - textPos, 0))
	screen.blit(boostStrip, (0, HEIGHT // 2))
	pygame.display.update()

pygame.quit()