
import logging, pigpio

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import mainthread

from .bus import bus
from .gpio import pi
from .Config import Config
from .Settings import Settings
from .BackgroundLabel import BackgroundLabel
from .ImageButton import ImageButton
from .ConfirmDialog import ConfirmDialog


Builder.load_string('''
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
''')

    
class OutputCounter(RelativeLayout):

    MaxCount = 9999
    PortDebounce = 1000
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = Config.config()
        settings = Settings.settings()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.sensorPort = config.getint('core', 'outputCounterPort')
        
        self.setupGPIO()

        self.running = True
        self.sensorTriggered = pi.read(self.sensorPort) == pigpio.HIGH
        self.count = settings.getint('session', 'outputCount', fallback = 0)
        
        bus.add_event(self.reset, 'reset')
        
        self.update()
        bus.emit('outputCounter/count', self.count, True)
        
    def setupGPIO(self):
        
        def cb(port, level, tick):
            self.sensorTriggered = level == 1
            if level == 0 and self.running == True:
                self.change_count(1, False)
            else:
                self.update()
            
        pi.set_mode(self.sensorPort, pigpio.INPUT)
        pi.set_pull_up_down(self.sensorPort, pigpio.PUD_UP)
        pi.set_glitch_filter(self.sensorPort, self.PortDebounce)
        self.cb = pi.callback(self.sensorPort, pigpio.EITHER_EDGE, cb)

    def on_press_playPause(self):
        self.running = not self.running
            
    def on_release_playPause(self):
        self.update()
        
    def on_press_plus(self):
        self.change_count(1, True)

    def on_long_press_plus(self, inst, count):
        delta = 1 if count < 10 else 10 if count < 20 else 100
        self.change_count(delta, True)
    
    def on_press_minus(self):
        self.change_count(-1, True)
        
    def on_long_press_minus(self, inst, count):
        delta = -1 if count < 10 else -10 if count < 20 else -100
        self.change_count(delta, True)

    def change_count(self, delta, manual):
        self.count = min(max(self.count + delta, 0), self.MaxCount)
        self.update()
        bus.emit('outputCounter/count', self.count, manual)
        Settings.settings().safe_set('session', 'outputCount', self.count)
    
    def on_count_long_press(self):
        if self.count == 0: return
        ConfirmDialog(text = 'Are you sure you want to reset the count?', on_confirm = self.reset)
    
    def reset(self, *args):
        self.running = True
        self.sensorTriggered = pi.read(self.sensorPort) == pigpio.HIGH
        self.count = 0
        self.update()
        bus.emit('outputCounter/count', self.count, True)
        Settings.settings().safe_set('session', 'outputCount', self.count)
    
    @mainthread
    def update(self):
        self.playPauseImage = 1 if self.running else 0
        self.sensorImage = 1 if self.sensorTriggered else 0
        self.countStr = str(self.count)
        
