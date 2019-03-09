
import logging, pigpio

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import mainthread, Clock

from .bus import bus
from .gpio import pi
from .Config import Config


KV = '''
<SimpleSensor>:
    background_text: 'Change me'
    sensor_image: 0
    
    BackgroundLabel:
        text: self.parent.background_text
        font_size: self.height * 0.45
        halign: 'center'
        
    BoxLayout:
        orientation: 'horizontal'
        Label:
        MultiImage:
            images: 'empty.png', 'flash.png', 'alert.png'
            image_idx: self.parent.parent.sensor_image
            size_hint_x: None
            width: self.height
        Label:
'''

class SimpleSensor(RelativeLayout):

    PortDebounce = 1000

    def __init__(self, type, name, triggerLevel, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        config = Config.config()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.type = type
        self.triggerLevel = triggerLevel
        self.sensorPort = config.getint('core', self.type + 'SensorPort')
        self.sensorTriggered = False
        self.blinkOn = True
        self.sensorTriggeredTimeout = config.getfloat('core', self.type + 'SensorTriggeredTimeout')
        
        self.setupGPIO()
        
        self.sensorTriggeredTimer = Clock.create_trigger(self.on_sensorTriggered, self.sensorTriggeredTimeout)
        self.blinkTimer = Clock.schedule_interval(self.on_blink, 0.25)
        self.blinkTimer.cancel()
        
        def cb(dt):
            self.background_text = name
            if pi.read(self.sensorPort) == self.triggerLevel:
                self.sensorTriggered = True
                self.sensorTriggeredTimer()
                
        Clock.schedule_once(cb)
        
        self.update()

    def setupGPIO(self):
        
        def cb(port, level, tick):
            self.sensorTriggered = level == self.triggerLevel
            
            if level == self.triggerLevel:
                self.sensorTriggeredTimer.cancel()
                self.sensorTriggeredTimer()
                
            else:
                self.sensorTriggeredTimer.cancel()
                if self.blinkTimer.is_triggered:
                    self.stop_alert()
                    
            self.update()
            
        pi.set_mode(self.sensorPort, pigpio.INPUT)
        pi.set_pull_up_down(self.sensorPort, pigpio.PUD_UP)
        pi.set_glitch_filter(self.sensorPort, self.PortDebounce)
        self.cb = pi.callback(self.sensorPort, pigpio.EITHER_EDGE, cb)

    def start_alert(self):
        self.blinkTimer.cancel()
        self.blinkTimer()
        self.blinkOn = True
        bus.emit(self.type + 'Sensor/set')

    def stop_alert(self):
        self.blinkTimer.cancel()
        bus.emit(self.type + 'Sensor/clear')

    def on_sensorTriggered(self, dt):
        self.start_alert()
        self.update()
        
    def on_blink(self, dt):
        self.blinkOn = not self.blinkOn
        self.update()
        
    @mainthread
    def update(self):
        if self.blinkTimer.is_triggered:
            self.sensor_image = 2 if self.blinkOn else 0
        elif self.sensorTriggered:
            self.sensor_image = 1
        else:
            self.sensor_image = 0
        