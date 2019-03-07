
import logging, logging.handlers, re

from .Config import Config


_levelPattern = re.compile(r"^level\.(.*)")


def configureLogging():
    config = Config.config()
    
    root = logging.getLogger()
    root.setLevel(getattr(logging, config.get('logging', 'logLevel')))
    
    handler = logging.handlers.RotatingFileHandler(
        config.getpath('logging', 'logFile'),
        maxBytes = config.getint('logging', 'logSize'),
        backupCount = config.getint('logging', 'logCount'))
        
    handler.setFormatter(logging.Formatter(fmt = config.get('logging', 'logFormat')))
    root.addHandler(handler)

#    if config.getboolean('logging', 'console'):
#        handler = logging.StreamHandler()
#        handler.setFormatter(logging.Formatter(fmt = config.get('logging', 'logFormat')))
#        root.addHandler(handler)

    for (k, v) in config.items('logging'):
        m = _levelPattern.match(k)
        if m:
            logging.getLogger(m.group(1)).setLevel(getattr(logging, v))

