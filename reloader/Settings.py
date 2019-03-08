
import os, configparser

from .Config import Config


class Settings(configparser.ConfigParser):

    _settings = None
    
    @classmethod
    def settings(cls):
        if not cls._settings:
            cls._settings = Settings()
        return cls._settings
        
    def __init__(self):
        super().__init__(interpolation = None)
        self.optionxform = str
        self.clear()
        file = Config.config().getpath('core', 'settings')
        if os.path.isfile(file):
            self.read(file)
        
    def save(self):
        file = Config.config().getpath('core', 'settings')
        with open(file, 'w') as settings:
            self.write(settings)
    
