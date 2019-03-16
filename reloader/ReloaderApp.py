
import os, logging

from kivy.app import App
from kivy.resources import resource_add_path
from kivy.clock import Clock

from .bus import bus
from .Config import Config
from .Settings import Settings
from .ReloaderScreen import ReloaderScreen


class ReloaderApp(App):

    _app = None
    
    @classmethod
    def app(cls):
        if not cls._app:
            cls._app = ReloaderApp()
        return cls._app
        
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.saveEvent = None
        self.logger.info('Application initialized')

    def build(self):
        resource_add_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources'))
        screen = ReloaderScreen.screen()
        self.saveEvent = Clock.schedule_interval(Settings.settings().save, Config.config().getfloat('core', 'settingsSaveInterval'))
        bus.emit('app/start')
        return screen


        