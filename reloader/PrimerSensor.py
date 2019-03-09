
import logging, pigpio

from .SimpleSensor import SimpleSensor


class PrimerSensor(SimpleSensor):

    def __init__(self, **kwargs):
        super().__init__('primer', 'Primers', pigpio.LOW, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
