
import logging

from .Collator import Collator


class BulletCollator(Collator):

    def __init__(self, **kwargs):
        super().__init__('bullet', **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
