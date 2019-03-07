
import logging

from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

from reloader.TitleBar import TitleBar
from reloader.Timer import Timer
from reloader.OutputRate import OutputRate
from reloader.CaseCollator import CaseCollator
from reloader.BulletCollator import BulletCollator
from reloader.OutputCounter import OutputCounter


KV = '''
<ReloaderScreen>:
    cols: 1
    TitleBar:
        height: '40sp'
        size_hint_y: None
    Timer:
        height: '100sp'
        size_hint_y: None
    OutputRate:
        height: '100sp'
        size_hint_y: None
    CaseCollator:
        height: '100sp'
        size_hint_y: None
    BulletCollator:
        height: '100sp'
        size_hint_y: None
    OutputCounter:
        height: '120sp'
        size_hint_y: None
    
'''

class ReloaderScreen(GridLayout):

    _screen = None
    
    @classmethod
    def screen(cls):
        if not cls._screen:
            cls._screen = ReloaderScreen()
        return cls._screen
        
    def __init__(self):
        Builder.load_string(KV)
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)


        