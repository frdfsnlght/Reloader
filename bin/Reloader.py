#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reloader.Config import Config
from reloader.logging import configureLogging
from reloader.ReloaderApp import ReloaderApp


if __name__ == '__main__':
    configureLogging()
    app = ReloaderApp.app()
    try:
        app.run()
    except KeyboardInterrupt:
        pass
        





