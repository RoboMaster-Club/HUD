#!/usr/bin/env python
import pygame
import serial

# Initialization
pygame.init()

# Screen Constants
RESOLUTION = WIDTH, HEIGHT = (480, 320)
SCREEN_MARGIN = 30
FRAME_RATE = 30

# Boost Strip
# Dimension of rectangle
BOOSTSTRIP_WIDTH = 15
BOOSTSTRIP_HEIGHT = 200
BOOSTSTRIP_TOP = (HEIGHT + BOOSTSTRIP_HEIGHT) // 2
BOOSTSTRIP_LEFT = WIDTH - SCREEN_MARGIN - BOOSTSTRIP_WIDTH

# Strip configuration
BOOSTSTRIP_COLOR = pygame.Color(150, 0, 0, 10)

# Strip Frame
BOOSTSTRIP_FRAME_WIDTH = 5
BOOSTSTRIP_FRAME_COLOR = pygame.Color(255, 255, 255)
BOOSTSTRIP_FRAME = pygame.Rect(BOOSTSTRIP_LEFT - BOOSTSTRIP_FRAME_WIDTH, 
								BOOSTSTRIP_TOP + BOOSTSTRIP_FRAME_WIDTH,
								BOOSTSTRIP_WIDTH + 2 * BOOSTSTRIP_FRAME_WIDTH, 
								-(BOOSTSTRIP_HEIGHT + 2 * BOOSTSTRIP_FRAME_WIDTH))

# Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Font
class TextFormatter():
	def __init__(self, font, textColor=(255, 255, 255)):
		"""
		TextFormatter Constructer

		@param font: pygame.font.Font
		@param textColor: color of the string
		"""
		self.font = font
		self.textColor = textColor
	
	def format(self, formatString, startPos=(0, 0)):
		"""
		Create formatted text surface object

		@param string: string contains new line character
		@param startPos: Position of the final output text block, 
						first is the right position, second is the bottom
		@return textSurfaces: list of tuples containing textSurface object and its position
		"""
		strings = formatString.split("\n")
		textSurfaces = []
		startRight = startPos[0]
		startBottom = startPos[1]
		relativeBottom = 0
		for string in strings:
			textSurface, textSize = self._render(string)
			textPos = (startRight - textSize[0], startBottom + relativeBottom)
			textSurfaces.append((textSurface, textPos))
			relativeBottom += textSize[1] 
		return textSurfaces



	def _render(self, string):
		"""
		Simple renderer wrapper

		@param font: pygame.font.Font
		@param string: string to put on screen
		@return textSurface: pygame.Surface object of the string
		@return textSize: size of text in pixels
		"""
		textSurface = self.font.render(string, False, self.textColor)
		textSize = self.font.size(string)

		return textSurface, textSize

textfont = pygame.font.Font('./resource/fonts/RobotSlab/RobotoSlab-Thin.ttf', 15)
textFormatter = TextFormatter(textfont, WHITE)

# Serial Configuration
ser = serial.Serial()
ser.port = '/dev/cu.usbserial-00000000'
ser.timeout = 0.01  # Reading Timeout is 10 ms
ser.baudrate = 19200
maxTrials = 5

# Data communication
MaxCapVolt = 24

# Buckle Up!
screen = pygame.display.set_mode(RESOLUTION)
ser.open()

running = True
clock = pygame.time.Clock()
capVolt = 0
while running:
	# Run loop at most FRAME_RATE per seconds
	clock.tick(FRAME_RATE)

	# #--------------------------------
	# # Event handling
	# #--------------------------------
	# # TODO: Read from Serial and decode data communication
	# # Use comma for separation
	# data = None
	# tried = 0
	# while tried < 0:
	# 	tried += 1
	# 	# Try how many times
	# 	raw_data = ser.readline()
	# 	if not raw_data:
	# 		continue
	# 	else:
	# 		try:
	# 			data = raw_data.decode().split(',')
	# 			n = len(data)
	# 			data = [(data[i], data[i + 1]) for i in range(0, n, 2)] 
	# 			data = dict(data)
	# 			break
	# 		except BaseException:
	# 			continue
	# else:
	# 	pass
	# data = {'capVolt':'1'}
	capVolt = 1
	

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
	fps = clock.get_fps()
	time = clock.get_rawtime()

	sensorData = "FPS: %.2f\nTime: %.2f\nCapVolt: %.2f" % (fps, time / 1000, capVolt)

	# Text renderers
	# Align to the strip
	textSurfaces = textFormatter.format(sensorData, (WIDTH - SCREEN_MARGIN - BOOSTSTRIP_WIDTH - 10, (HEIGHT - BOOSTSTRIP_HEIGHT) // 2))


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
	screen.blit(flipped, (0, 0))
	pygame.display.update()

pygame.quit()