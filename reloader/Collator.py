
import logging, pigpio

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock, mainthread

from .bus import bus
from .gpio import pi
from .Config import Config
from .Settings import Settings
from .BackgroundLabel import BackgroundLabel
from .ButtonLabel import ButtonLabel
from .MultiImageButton import MultiImageButton
from .ImageButton import ImageButton
from .MultiImage import MultiImage
from .ConfirmDialog import ConfirmDialog
from .MotorSpeedDialog import MotorSpeedDialog


KV = '''
<Collator>:
    countStr: ''
    running: False
    playPauseImage: 0
    sensorImage: 0
    background_text: 'Change me'
    
    BackgroundLabel:
        text: self.parent.background_text
        
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
                padding: self.width * 0.05, self.height * 0.05
                on_press: self.parent.parent.parent.on_press_playPause()
                on_release: self.parent.parent.parent.on_release_playPause()
                on_long_press: self.parent.parent.parent.on_long_press_playPause()
                long_press_interval: 0
            ImageButton:
                image_normal: 'plus_normal.png'
                image_down: 'plus_down.png'
                on_press: self.parent.parent.parent.on_press_plus()
                on_long_press: self.parent.parent.parent.on_long_press_plus(*args)
            MultiImage:
                images: 'empty.png', 'flash.png', 'stop.png', 'alert.png'
                image_idx: self.parent.parent.parent.sensorImage
            ImageButton:
                image_normal: 'minus_normal.png'
                image_down: 'minus_down.png'
                on_press: self.parent.parent.parent.on_press_minus()
                on_long_press: self.parent.parent.parent.on_long_press_minus(*args)
'''

        
class Collator(RelativeLayout):

    MaxCount = 9999
    PortDebounce = 1000
    
    def __init__(self, type, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        config = Config.config()
        settings = Settings.settings()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.type = type
        self.running = False
        self.count = 0
        self.sensorTriggered = False
        self.blinkOn = True
        self.emptyTimeout = config.getfloat('core', self.type + 'CollatorEmptyTimeout')
        self.sensorPort = config.getint('core', self.type + 'SensorPort')
        self.motorPort = config.getint('core', self.type + 'MotorPort')
        self.motorFrequency = config.getint('core', self.type + 'MotorFrequency')
        self.motorDutycycle = settings.getint('collators', self.type + 'MotorSpeed', fallback = 100)
        self.resetConfirmDialog = None
        self.motorSpeedDialog = None
        
        self.setupGPIO()

        self.collatorEmptyTimer = Clock.create_trigger(self.on_collatorEmpty, self.emptyTimeout)
        self.outputFullTimer = Clock.create_trigger(self.on_outputFull, 0.5)
        self.blinkTimer = Clock.schedule_interval(self.on_blink, 0.25)
        self.blinkTimer.cancel()
        
        def cb(dt):
            self.background_text = self.type.capitalize() + 's'
            if pi.read(self.sensorPort) == pigpio.LOW:
                self.start_motor()
            else:
                self.sensorTriggered = True
                
        Clock.schedule_once(cb)
            
        self.update()
        bus.emit(self.type + 'Collator/count', self.count, True)
            
        
    def setupGPIO(self):
        
        def cb(port, level, tick):
            self.sensorTriggered = level == 1
            self.collatorEmptyTimer.cancel()
            self.collatorEmptyTimer()
            
            if level == 1:
                self.count = (self.count + 1) % self.MaxCount
                self.outputFullTimer.cancel()
                self.outputFullTimer()
                bus.emit(self.type + 'Collator/count', self.count, False)
                
            elif level == 0:
                self.outputFullTimer.cancel()
                if not self.running:
                    self.start_motor()
                    
            self.update()
            
        pi.set_mode(self.sensorPort, pigpio.INPUT)
        pi.set_pull_up_down(self.sensorPort, pigpio.PUD_UP)
        pi.set_glitch_filter(self.sensorPort, self.PortDebounce)
        self.cb = pi.callback(self.sensorPort, pigpio.EITHER_EDGE, cb)

        pi.set_mode(self.motorPort, pigpio.OUTPUT)
        pi.set_PWM_range(self.motorPort, 100)
        pi.set_PWM_dutycycle(self.motorPort, 0)
        pi.set_PWM_frequency(self.motorPort, self.motorFrequency)
            
    def start_motor(self):
        pi.set_PWM_dutycycle(self.motorPort, self.motorDutycycle)
        self.running = True
        self.collatorEmpty = False
        self.collatorEmptyTimer()
        self.stop_alert()
        bus.emit(self.type + 'Collator/running')
        
    def stop_motor(self):
        pi.set_PWM_dutycycle(self.motorPort, 0)
        self.running = False
        self.collatorEmptyTimer.cancel()
        bus.emit(self.type + 'Collator/stopped')

    def start_alert(self):
        self.blinkTimer.cancel()
        self.blinkTimer()
        self.blinkOn = True

    def stop_alert(self):
        self.blinkTimer.cancel()
        bus.emit(self.type + 'Collator/clear')
    
    def on_outputFull(self, dt):
        self.stop_motor();
        self.outputFullTimer.cancel()
        self.update()
        
    def on_collatorEmpty(self, dt):
#        print(self.type + ' empty')
        self.stop_motor()
        self.collatorEmpty = True
        self.start_alert()
        self.update()
        bus.emit(self.type + 'Collator/empty')
        
    def on_blink(self, dt):
        self.blinkOn = not self.blinkOn
        self.update()
        
    def on_press_playPause(self):
        if self.running:
            self.stop_motor()
        else:
            self.start_motor()
            
    def on_release_playPause(self):
        self.update()
        
    def on_long_press_playPause(self):
        self.stop_alert()
        if not self.motorSpeedDialog:
            self.motorSpeedDialog = MotorSpeedDialog()
            self.motorSpeedDialog.title = self.type.capitalize() + ' Motor'
            self.motorSpeedDialog.slider.bind(value = self.on_change_motorSpeed)
            self.motorSpeedDialog.bind(on_dismiss = self.on_dismiss_motorSpeed)
        self.motorSpeedDialog.slider.value = self.motorDutycycle
        self.motorSpeedDialog.open()

    def on_change_motorSpeed(self, inst, value):
        self.motorDutycycle = int(value)
        if self.running:
            pi.set_PWM_dutycycle(self.motorPort, self.motorDutycycle)

    def on_dismiss_motorSpeed(self, inst):
        settings = Settings.settings()
        if not settings.has_section('collators'):
            settings.add_section('collators')
        settings.set('collators', self.type + 'MotorSpeed', str(self.motorDutycycle))
        settings.save()
            
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
        self.stop_alert()
        self.update()
        bus.emit(self.type + 'Collator/count', self.count, True)
    
    def on_count_long_press(self):
        self.stop_alert()
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
        if self.blinkTimer.is_triggered:
            self.sensorImage = 3 if self.blinkOn else 0
        elif self.sensorTriggered:
            self.sensorImage = 1 if self.outputFullTimer.is_triggered else 2
        else:
            self.sensorImage = 0
        self.countStr = str(self.count)
        