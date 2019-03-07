
import os, logging

from kivy.app import App
from kivy.resources import resource_add_path

from reloader.Config import Config
from reloader.ReloaderScreen import ReloaderScreen


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
        self.logger.info('Application initialized')

    def build(self):
        resource_add_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources'))
        screen = ReloaderScreen.screen()
        return screen


        