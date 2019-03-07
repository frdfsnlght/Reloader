
import logging, pigpio

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import mainthread

from reloader.bus import bus
from reloader.gpio import pi
from reloader.Config import Config
from reloader.BackgroundLabel import BackgroundLabel
from reloader.ImageButton import ImageButton
from reloader.ConfirmDialog import ConfirmDialog


KV = '''
<OutputCounter>:
    countStr: ''
    
    BackgroundLabel:
        text: 'Output'
        
    BoxLayout:
        orientation: 'horizontal'
        spacing: self.height * 0.06
        Label:
            text: self.parent.parent.countStr
            text_size: self.size
            font_size: self.height * 0.9
            halign: 'right'
            max_lines: 1
            padding_y: self.height * 0.15
        GridLayout:
            cols: 2
            size_hint_x: None
            width: self.parent.height
            ImageButton:
                image_normal: 'plus_normal.png'
                image_down: 'plus_down.png'
                on_press: self.parent.parent.parent.on_press_plus()
            ImageButton:
                image_normal: 'reset_normal.png'
                image_down: 'reset_down.png'
                on_press: self.parent.parent.parent.on_press_reset()
            ImageButton:
                image_normal: 'minus_normal.png'
                image_down: 'minus_down.png'
                on_press: self.parent.parent.parent.on_press_minus()
'''

        
class OutputCounter(RelativeLayout):

    MaxCount = 9999
    PortDebounce = 1000
    
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.count = 0
        self.resetConfirmDialog = None
        self.update()
        self.startGPIO()
        bus.emit('outputCounter/count', self.count, True)
        
    def startGPIO(self):
        config = Config.config()
        port = config.getint('core', 'outputCounterPort')
        
        def cb(port, level, tick):
            self.count = (self.count + 1) % self.MaxCount
            self.update()
            bus.emit('outputCounter/count', self.count, False)
            
        pi.set_mode(port, pigpio.INPUT)
        pi.set_pull_up_down(port, pigpio.PUD_UP)
        pi.set_glitch_filter(port, self.PortDebounce)
        self.cb = pi.callback(port, pigpio.FALLING_EDGE, cb)

    def on_press_plus(self):
        self.count = min(self.count + 1, self.MaxCount)
        self.update()
        bus.emit('outputCounter/count', self.count, True)
    
    def on_press_minus(self):
        self.count = max(self.count - 1, 0)
        self.update()
        bus.emit('outputCounter/count', self.count, True)
    
    def on_press_reset(self):
        if self.count == 0: return
        if not self.resetConfirmDialog:
            self.resetConfirmDialog = ConfirmDialog()
            self.resetConfirmDialog.text = 'Are you sure you want to reset the count?'
            self.resetConfirmDialog.bind(on_dismiss = self.on_dismiss_reset)
        self.resetConfirmDialog.open()
    
    def on_dismiss_reset(self, inst):
        if inst.confirmed:
            self.count = 0
            self.update()
            bus.emit('outputCounter/count', self.count, True)
    
    @mainthread
    def update(self):
        self.countStr = str(self.count)
        