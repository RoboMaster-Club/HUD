from serial.threaded import ReaderThread
from config import SerialCommunicationConfiguration


serial_config = SerialCommunicationConfiguration(serial_port='/dev/cu.usbserial-00000000')
serial_interface = serial_config.get_serial()
protocol = serial_config.get_protocol()
buffer = serial_config.get_buffer()
serialThread = ReaderThread(serial_interface, protocol)
serialThread.start()


while True:
    print(buffer.get())
