import serial
from serial.threaded import LineReader, ReaderThread
from queue import LifoQueue, Full, Empty
import os
import sys


BUFFER_SIZE = 100
bufferQueue = LifoQueue(BUFFER_SIZE)


class ReadData(LineReader):
    def connection_made(self, transport):
        super(ReadData, self).connection_made(transport)
        sys.stdout.write('port opened\n')

    def handle_line(self, data):
        # sys.stdout.write('line received: {}\n'.format(repr(data)))
        try:
            bufferQueue.put_nowait(data)
        except Full:
            with bufferQueue.mutex:
                # Safely flush the buffer
                bufferQueue.queue.clear()
            bufferQueue.put_nowait(data)

    def connection_lost(self, exc):
        sys.stdout.write('port closed\n')


ser = serial.Serial()
ser.port = '/dev/cu.usbserial-00000000'
ser.timeout = 1  # Reading Timeout is 10 ms
ser.baudrate = 19200
ser.parity = serial.PARITY_EVEN
ser.open()
serialThread = ReaderThread(ser, ReadData)
serialThread.start()
transport, protocol = serialThread.connect()

while True:
    try:
        print(bufferQueue.get_nowait())
    except Empty:
        continue
