from serial.threaded import FramedPacket
from queue import LifoQueue, Full, Empty
import struct
import sys


# Screen Constants
RESOLUTION = WIDTH, HEIGHT = 480, 320
SCREEN_MARGIN = 30
FRAME_RATE = 144

# Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Boost Strip
# Dimension of rectangle
MaxCapVolt = 24
BOOSTSTRIP_WIDTH = 15
BOOSTSTRIP_HEIGHT = 200
BOOSTSTRIP_TOP = (HEIGHT + BOOSTSTRIP_HEIGHT) // 2
BOOSTSTRIP_LEFT = WIDTH - SCREEN_MARGIN - BOOSTSTRIP_WIDTH

# Strip configuration
BOOSTSTRIP_COLOR = WHITE

# Strip Frame
BOOSTSTRIP_FRAME_WIDTH = 1


class TextFormatter:
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


# Serial Communication
BUFFER_SIZE = 100
bufferQueue = LifoQueue(BUFFER_SIZE)


# TODO Redefine terminator char
# TODO Upack incoming cstruct
dataName = ['capVolt', 'time', 'sample']


class ReadData(FramedPacket):
    START = b'('
    STOP = b')'
    DATAFORMAT = 'fff'

    def connection_made(self, transport):
        super(ReadData, self).connection_made(transport)
        sys.stdout.write('port opened\n')

    def handle_packet(self, data):
        data = struct.unpack(self.DATAFORMAT, data)
        try:
            bufferQueue.put_nowait(data)
        except Full:
            with bufferQueue.mutex:
                # Safely flush the buffer
                bufferQueue.queue.clear()
            bufferQueue.put_nowait(data)

    def connection_lost(self, exc):
        sys.stdout.write('port closed\n')