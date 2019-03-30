from io import TextIOBase
from time import sleep, clock
from threading import Thread
from luma.emulator.device import pygame, capture
from luma.core.render import canvas

"""
Error module
Define error io
TODO Extend TextIO class, file object
Interface defintion: https://docs.python.org/3/library/io.html#module-io
"""


# TODO Classify into display module?
# TODO Rolling display?
# TODO Use another thread to continuously render the oled
class OLEDTextIO(TextIOBase):
    """
    Provide wrapper to display message on oled or oled emulator based on luma.core.device.device
    """
    encoding = 'utf8'
    def __init__(self, device, fps=30):
        super(TextIOBase, self).__init__()
        self.DEVICE = device
        self.FPS = fps
        self.TIME_TICK = 1 / fps
        self.stop_drawing = False
        self.isRunning = False
        self.drawing_thread = Thread()
        self.text = ""

    def write(self, xy, text, *args, **kwargs):
        self.text = text
        if self.isRunning:
            self.stop_drawing = True
            self.drawing_thread.join()
            self.stop_drawing = False
        else:
            self.isRunning = True
        params = [xy, text]
        args = args if len(args) > 0 else []
        params.extend(args)
        args = tuple(params)
        self.drawing_thread = Thread(target=self._renderer, args=args, kwargs=kwargs)
        self.drawing_thread.start()

    # TODO Implement read method to read text buffer
    def readable(self, *args, **kwargs):
        return True

    def seekable(self, *args, **kwargs):
        return False

    def writable(self, *args, **kwargs):
        return True

    def _renderer(self, xy, text, *args, **kwargs):
        """
        Render the text on oled in a separate thread
        :return:
        """
        while not self.stop_drawing:
            # Continue render text
            with canvas(self.DEVICE) as draw:
                draw.text(xy, text, *args, **kwargs)
            sleep(self.TIME_TICK)
            print(clock(), text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drawing_thread.join()


if __name__ == "__main__":
    start = clock()
    oled = pygame()
    dummy = OLEDTextIO(oled)
    while True:
        dummy.write((0, 0), "Test", fill="White")
        sleep(2)
        dummy.write((100, 0), "Hellow", fill="White")
        sleep(2)
