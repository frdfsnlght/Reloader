
import logging, pigpio

from .SimpleSensor import SimpleSensor


class PowderSensor(SimpleSensor):

    def __init__(self, **kwargs):
        super().__init__('powder', 'Powder', pigpio.LOW, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
