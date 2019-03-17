
import subprocess

from kivy.lang.builder import Builder
#from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView

from .bus import bus
from .Config import Config


Builder.load_string('''
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
''')

class PowerDialog(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open()
        
    def on_press_shutdown(self):
        self.dismiss()
        config = Config.config()
        bus.emit('power/shutdown')
        self.run_command(config.get('commands', 'shutdown'))
                
    def on_press_restart(self):
        self.dismiss()
        config = Config.config()
        bus.emit('power/restart')
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
