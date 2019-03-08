
import logging

from .Collator import Collator


class CaseCollator(Collator):

    def __init__(self, **kwargs):
        super().__init__('case', **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
