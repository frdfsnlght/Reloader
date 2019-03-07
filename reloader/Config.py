
import os, configparser


_rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ['KIVY_NO_FILELOG'] = '1'
#os.environ['KIVY_NO_CONSOLELOG'] = '1'
os.environ['KIVY_NO_ARGS'] = '1'
KIVY_CONFIG = os.path.join(_rootDir, 'etc', 'kivy.ini')
if os.path.isfile(KIVY_CONFIG):
    os.environ['KIVY_USE_DEFAULTCONFIG'] = '1'
    from kivy.config import Config
    Config.read(KIVY_CONFIG)
import kivy


class Config(configparser.ConfigParser):

    _config = None
    
    @classmethod
    def config(cls):
        if not cls._config:
            cls._config = Config()
        return cls._config
        
    def __init__(self, fileBase = 'config'):
        super().__init__(interpolation = None, converters = {'path': self.resolvePath})
        self.optionxform = str    # preserve option case
        self.clear()
        
        defaultFile = os.path.join(_rootDir, 'etc', fileBase + '-default.ini')
        localFile = os.path.join(_rootDir, 'etc', fileBase + '.ini')
        
        if os.path.isfile(defaultFile):
            self.read(defaultFile)
        if os.path.isfile(localFile):
            self.read(localFile)
        
    def resolvePath(self, str):
        str = os.path.expanduser(str)
        if os.path.isabs(str):
            return str
        else:
            return os.path.normpath(os.path.join(_rootDir, str))
    
