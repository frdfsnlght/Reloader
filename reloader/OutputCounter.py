
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
    playPauseImage: 0
    sensorImage: 0
    
    BackgroundLabel:
        text: 'Output'
        
    BoxLayout:
        orientation: 'horizontal'
        spacing: self.height * 0.06
        ButtonLabel:
            text: self.parent.parent.countStr
            text_size: self.size
            font_size: self.height * 0.9
            halign: 'right'
            max_lines: 1
#            padding_y: self.height * 0.15
            on_long_press: self.parent.parent.on_count_long_press()
        GridLayout:
            cols: 2
            size_hint_x: None
            width: self.parent.height
            MultiImageButton:
                images_normal: 'play_normal.png', 'pause_normal.png'
                images_down: 'play_down.png', 'pause_down.png'
                image_set: self.parent.parent.parent.playPauseImage
                on_press: self.parent.parent.parent.on_press_playPause()
                on_release: self.parent.parent.parent.on_release_playPause()
            ImageButton:
                image_normal: 'plus_normal.png'
                image_down: 'plus_down.png'
                on_press: self.parent.parent.parent.on_press_plus()
                on_long_press: self.parent.parent.parent.on_long_press_plus(*args)
            MultiImage:
                images: 'empty.png', 'flash.png'
                image_idx: self.parent.parent.parent.sensorImage
            ImageButton:
                image_normal: 'minus_normal.png'
                image_down: 'minus_down.png'
                on_press: self.parent.parent.parent.on_press_minus()
                on_long_press: self.parent.parent.parent.on_long_press_minus(*args)
'''

        
class OutputCounter(RelativeLayout):

    MaxCount = 9999
    PortDebounce = 1000
    
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.count = 0
        self.running = True
        self.sensorTriggered = False
        self.resetConfirmDialog = None
        self.update()
        self.startGPIO()
        bus.emit('outputCounter/count', self.count, True)
        
    def startGPIO(self):
        config = Config.config()
        port = config.getint('core', 'outputCounterPort')
        
        def cb(port, level, tick):
            self.sensorTriggered = level == 1
            if level == 0 and self.running == True:
                self.count = (self.count + 1) % self.MaxCount
                bus.emit('outputCounter/count', self.count, False)
            self.update()
            
        pi.set_mode(port, pigpio.INPUT)
        pi.set_pull_up_down(port, pigpio.PUD_UP)
        pi.set_glitch_filter(port, self.PortDebounce)
        self.cb = pi.callback(port, pigpio.EITHER_EDGE, cb)

    def on_press_playPause(self):
        self.running = not self.running
            
    def on_release_playPause(self):
        self.update()
        
    def on_press_plus(self):
        self.change_count(1)

    def on_long_press_plus(self, inst, count):
        delta = 1 if count < 10 else 10 if count < 20 else 100
        self.change_count(delta)
    
    def on_press_minus(self):
        self.change_count(-1)
        
    def on_long_press_minus(self, inst, count):
        delta = -1 if count < 10 else -10 if count < 20 else -100
        self.change_count(delta)

    def change_count(self, delta):
        self.count = min(max(self.count + delta, 0), self.MaxCount)
        self.update()
        bus.emit('outputCounter/count', self.count, True)
    
    def on_count_long_press(self):
#    def on_press_reset(self):
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
        self.playPauseImage = 1 if self.running else 0
        self.sensorImage = 1 if self.sensorTriggered else 0
        self.countStr = str(self.count)
        
