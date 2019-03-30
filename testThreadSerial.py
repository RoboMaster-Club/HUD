import serial
from serial.threaded import FramedPacket, ReaderThread
from queue import LifoQueue, Full, Empty
import os
import struct
import sys


BUFFER_SIZE = 100
bufferQueue = LifoQueue(BUFFER_SIZE)


class ReadData(FramedPacket):
    START = b'('
    STOP = b')'
    DATAFORMAT = 'fff'


    def connection_made(self, transport):
        super(ReadData, self).connection_made(transport)
        sys.stdout.write('port opened\n')

    def handle_packet(self, data):
        # sys.stdout.write('line received: {}\n'.format(repr(data)))
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


ser = serial.Serial()
ser.port = '/dev/cu.usbserial-00000000'
ser.timeout = 1  # Reading Timeout is 10 ms
ser.baudrate = 115200
ser.parity = serial.PARITY_EVEN
ser.open()
serialThread = ReaderThread(ser, ReadData)
serialThread.start()
transport, protocol = serialThread.connect()

while True:
    try:
        print(struct.unpack('hhh', bufferQueue.get_nowait()))
    except Empty:
        continue
