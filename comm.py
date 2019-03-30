from serial.threaded import FramedPacket
from queue import LifoQueue, Full
import struct
import sys

"""
Communication module
"""


class StructReader(FramedPacket):
    """
    Parsing c-struct bytes data
    """
    def __init__(self, start, end, data_format, buffer, port_open_msg="Port opened\n",
                 port_close_msg="Port closed\n", stdin_fp=sys.stdin, stdout_fp=sys.stdout,
                 stderr_fp=sys.stderr):
        super().__init__()
        if not isinstance(buffer, LifoQueue):
            raise TypeError("Buffer should be an instance of LifoQueue from queue module")
        else:
            self.START = start
            self.END = end
            self.DATA_FORMAT = data_format
            self.BUFFER = buffer
            self.PORT_OPEN_MSG = port_open_msg
            self.PORT_CLOSE_MSG = port_close_msg
            self.STDIN = stdin_fp
            self.STDOUT = stdout_fp
            self.STDERR = stderr_fp
            super_scheme = super.__dict__
            scheme = self.__dict__

            class StructReaderPrototype(StructReader):
                def __init__(self):
                    self.__dict__.update(super_scheme)
                    self.__dict__.update(scheme)
            self.PROTOTYPE = StructReaderPrototype

    def get_prototype(self):
        return self.PROTOTYPE

    def connection_made(self, transport):
        super(StructReader, self).connection_made(transport)
        self.STDOUT.write(str(self.PORT_OPEN_MSG))

    def handle_packet(self, data):
        try:
            data = struct.unpack(self.DATA_FORMAT, data)
            self.BUFFER.put_nowait(data)
        except struct.error:
            return
        except Full:
            with self.BUFFER.mutex:
                # Safely flush the buffer
                self.BUFFER.queue.clear()
            self.BUFFER.put_nowait(data)

    def connection_lost(self, exc):
        self.STDERR.write(str(exc))
        self.STDOUT.write(str(self.PORT_CLOSE_MSG))
