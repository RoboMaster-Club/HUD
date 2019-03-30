from queue import LifoQueue
from serial import Serial, PARITY_EVEN
from comm import StructReader
import sys

"""
Configuration files
"""


class BaseConfiguration:
    def __init__(self, name="Base configuration class"):
        self.NAME = name

    def __str__(self):
        # TODO Cause `Fatal Python error: Cannot recover from stack overflow` in PyCharm debug mode.
        # properties = self.__dict__
        # string = "NAME: %s" % name
        # for key in properties:
        #     # % causes stack overflow
        #     string += key + ": " + str(properties[key]) + "\n"
        string = "NAME: " + self.NAME
        return string


class DisplayConfiguration(BaseConfiguration):
    """
    Oled Module configuration class
    """

    def __init__(self, i2c_port=1, i2c_address=0x3c, resolution=(128, 64), frame_rate=30,
                 name="OLED module configuration"):
        super().__init__(self)
        self.RESOLUTION = self.WIDTH, self.HEIGHT = resolution
        self.FRAME_RATE = frame_rate


class SerialCommunicationConfiguration(BaseConfiguration):
    """
    Serial communication moduel configuration class
    """

    def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, parity=PARITY_EVEN, timeout=None,
                 buffer=LifoQueue(100), reader=StructReader, start=b"(", end=b")", data_format="fff",
                 stdio_fp={}, name="Serial communication configuration"):
        super().__init__(self)
        self.BUFFER = buffer
        self.BUFFER_SIZE = self.BUFFER.maxsize
        self.START_CHAR = start
        self.END_CHAR = end
        self.DATA_FORMAT = data_format
        self.SERIAL = Serial(port=serial_port, baudrate=serial_baudrate, parity=parity, timeout=timeout)
        self.STDIO_FP = stdio_fp
        self.READER = reader

    def get_serial(self):
        """
        Get the serial interface
        :return Serial class configure by the init method:
        """
        return self.SERIAL

    def get_protocol(self):
        """
        Get the protocol for serial communication
        :return Subclass of serial.threaded.Packetizer:
        """
        return self.READER(self.START_CHAR, self.END_CHAR, self.DATA_FORMAT, self.BUFFER, **self.STDIO_FP).get_prototype()

    def get_buffer(self):
        """
        Get threading data buffer
        :return:
        """
        return self.BUFFER


class ConfigurationManagement:
    """
    Abstract class for module configuration
    """

    NAME = "Configuration interface"
    CURRENT_CONFIG = None
    DEFAULT_CONFIG = None

    def __init__(self):
        """
        Initialize configuration class
        """
        pass

    def get_config_list(self):
        """
        Get current configuration list
        :return: list of current configuration
        """
        pass

    def get_config(self, index):
        """
        Get a specific configuration
        :param index: index of the configuration
        :return: configuration struct / class
        """
        pass

    def get_current_config(self):
        """
        Get the current configuration used
        :return: configuration struct / class
        """
        return self.CURRENT_CONFIG

    def get_default_config(self):
        """
        Get the default configuration, usually store in class declaration
        :return:
        """
        return self.DEFAULT_CONFIG

    def set_config(self, index, new_config):
        """
        Set the designated configuration to the new_config
        :param index: index of the configuration, None to add new configuration
        :param new_config: new configuration struct / class, None to delete this configuration
        :return: None
        """
        pass

    def set_current_config(self, index=None, new_config=None):
        """
        Set the current configuration for module
        :param index: Index of configuration in the configuration list
        :param new_config: new configuration struct / class
        :return: None
        """
        pass

    def flush_configs(self):
        """
        Store configurations in the current list to storage
        :return:
        """
        pass

    def _read_configs(self):
        """
        Read configuration from storage
        :return: None
        """
        pass