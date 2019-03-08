
import logging

from .SimpleSensor import SimpleSensor


class PrimerSensor(SimpleSensor):

    def __init__(self, **kwargs):
        super().__init__('primer', 'Primers', **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
