#!/usr/bin/env python
import serial
from serial.threaded import ReaderThread
import platform
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
from luma.emulator.device import pygame
from PIL import ImageFont
from util import *

# Initialization
system = platform.system()

# Serial Configuration
# ser = serial.Serial()
# ser.port = '/dev/cu.usbserial-00000000' if system == 'Darwin' else '/dev/ttyS0'
# ser.baudrate = 115200
# ser.parity = serial.PARITY_EVEN
# ser.open()
#
# # Start serial data thread
# serialThread = ReaderThread(ser, ReadData)
# serialThread.start()


# Font Initialization
font = ImageFont.truetype('./resource/fonts/Roboto_Mono/RobotoMono-Thin.ttf', size=10)

# OLED initialization
if system == 'Darwin':
	oled = pygame()
else:
	oled_i2c = i2c(port=1, address=0x30)
	oled = ssd1309(oled_i2c)
FPS = 30
interval = 1 / 30


while True:
	sensorData = bufferQueue.get()

	with canvas(oled) as screen:
		screen.text((0, 0), 'Hello World!', font=font)
	time.sleep(interval)
# running = True
#
# while running:
# 	# Run loop at most FRAME_RATE per seconds

# serialThread.close()

