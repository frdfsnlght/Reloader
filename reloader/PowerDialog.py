
import subprocess

from kivy.lang.builder import Builder
#from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView

from .Config import Config


KV = '''
<PowerDialog>:
#    title: 'Power'
#    title_size: '20sp'
    size_hint: 0.6, 0.5
    
    BoxLayout:
        orientation: 'vertical'
        spacing: '20sp'
        padding: '20sp'
        Button:
            text: 'Shutdown'
            font_size: '20sp'
            on_press: self.parent.parent.on_press_shutdown()
        Button:
            text: 'Restart'
            font_size: '20sp'
            on_press: self.parent.parent.on_press_restart()
#        Button:
#            text: 'Restart X'
#            font_size: '20sp'
#            on_press: self.parent.parent.on_press_restartX()
'''

class PowerDialog(ModalView):

    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = PowerDialog()
        return cls._instance

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.isOpen = False
        
    def on_open(self):
        self.isOpen = True
        
    def on_dismiss(self):
        self.isOpen = False

    def on_press_shutdown(self):
        config = Config.config()
        self.run_command(config.get('commands', 'shutdown'))
                
    def on_press_restart(self):
        config = Config.config()
        self.run_command(config.get('commands', 'restart'))
    
#    def on_press_restartX(self):
#        config = Config.config()
#        self.run_command(config.get('commands', 'restartX'))

    def run_command(self, cmd):
        cmd = cmd.split(' ')
        out = subprocess.run(cmd,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
                universal_newlines = True)
        return out
