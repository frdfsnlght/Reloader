
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
        self.dirty = False
        
    # override
    def safe_set(self, section, key, value):
        if not self.has_section(section):
            self.add_section(section)
            self.dirty = True
        value = str(value)
        if self.get(section, key, fallback = None) != value:
            self.set(section, key, value)
            self.dirty = True
        
    def save(self, *args):
        if not self.dirty: return
        file = Config.config().getpath('core', 'settings')
        with open(file, 'w') as settings:
            self.write(settings)
    
