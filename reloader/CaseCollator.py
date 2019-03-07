
import logging, pigpio

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock, mainthread

from reloader.bus import bus
from reloader.gpio import pi
from reloader.Config import Config
from reloader.BackgroundLabel import BackgroundLabel
from reloader.MultiImageButton import MultiImageButton
from reloader.ImageButton import ImageButton
from reloader.MultiImage import MultiImage
from reloader.ConfirmDialog import ConfirmDialog
from reloader.MotorSpeedDialog import MotorSpeedDialog


KV = '''
<CaseCollator>:
    countStr: ''
    running: False
    playPauseImage: 0
    sensorImage: 0
    
    BackgroundLabel:
        text: 'Cases'
        
    BoxLayout:
        orientation: 'horizontal'
        spacing: self.height * 0.06
        Label:
            text: self.parent.parent.countStr
            text_size: self.size
            font_size: self.height * 0.9
            halign: 'right'
            max_lines: 1
#            padding_y: self.height * 0.15
        GridLayout:
            cols: 3
            size_hint_x: None
            width: self.parent.height * 1.5
            MultiImageButton:
                images_normal: 'play_normal.png', 'pause_normal.png'
                images_down: 'play_down.png', 'pause_down.png'
                image_set: self.parent.parent.parent.playPauseImage
                padding: self.width * 0.05, self.height * 0.05
                on_press: self.parent.parent.parent.on_press_playPause()
                on_release: self.parent.parent.parent.on_release_playPause()
            ImageButton:
                image_normal: 'plus_normal.png'
                image_down: 'plus_down.png'
                on_press: self.parent.parent.parent.on_press_plus()
            ImageButton:
                image_normal: 'reset_normal.png'
                image_down: 'reset_down.png'
                on_press: self.parent.parent.parent.on_press_reset()
            MultiImage:
                images: 'empty.png', 'flash.png', 'stop.png', 'alert.png'
                image_idx: self.parent.parent.parent.sensorImage
            ImageButton:
                image_normal: 'minus_normal.png'
                image_down: 'minus_down.png'
                on_press: self.parent.parent.parent.on_press_minus()
            ImageButton:
                image_normal: 'settings_normal.png'
                image_down: 'settings_down.png'
                on_press: self.parent.parent.parent.on_press_settings()
'''

        
class CaseCollator(RelativeLayout):

    MaxCount = 9999
    PortDebounce = 1000
    
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        config = Config.config()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.running = False
        self.count = 0
        self.sensorTriggered = False
        self.blinkOn = True
        self.emptyTimeout = config.getint('core', 'caseCollatorEmptyTimeout')
        self.sensorPort = config.getint('core', 'caseSensorPort')
        self.motorPort = config.getint('core', 'caseMotorPort')
        self.motorFrequency = config.getint('core', 'caseMotorFrequency')
        self.motorDutycycle = 100
        self.resetConfirmDialog = None
        self.motorSpeedDialog = None
        
        self.setupGPIO()

        self.collatorEmptyTimer = Clock.create_trigger(self.on_collatorEmpty, self.emptyTimeout)
        self.outputFullTimer = Clock.create_trigger(self.on_outputFull, 0.5)
        self.blinkTimer = Clock.schedule_interval(self.on_blink, 0.25)
        self.blinkTimer.cancel()
        
        self.update()
        
        def cb(dt):
            if pi.read(self.sensorPort) == pigpio.LOW:
                self.start_motor()
            else:
                self.sensorTriggered = True
                
        Clock.schedule_once(cb)
            
        self.update()
        bus.emit('caseCollator/count', self.count, True)
            
        
    def setupGPIO(self):
        config = Config.config()
        
        def cb(port, level, tick):
            self.sensorTriggered = level == 1
            self.collatorEmptyTimer.cancel()
            self.collatorEmptyTimer()
            
            if level == 1:
                self.count = (self.count + 1) % self.MaxCount
                self.outputFullTimer.cancel()
                self.outputFullTimer()
                bus.emit('caseCollator/count', self.count, False)
                
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
        bus.emit('caseCollator/running')
        
    def stop_motor(self):
        pi.set_PWM_dutycycle(self.motorPort, 0)
        self.running = False
        self.collatorEmptyTimer.cancel()
        bus.emit('caseCollator/stopped')

    def start_alert(self):
        self.blinkTimer.cancel()
        self.blinkTimer()
        self.blinkOn = True

    def stop_alert(self):
        self.blinkTimer.cancel()
    
    def on_outputFull(self, dt):
        self.stop_motor();
        self.outputFullTimer.cancel()
        self.update()
        
    def on_collatorEmpty(self, dt):
        self.stop_motor()
        self.collatorEmpty = True
        self.start_alert()
        self.update()
        bus.emit('caseCollator/empty')
        
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
        
    def on_press_plus(self):
        self.count = min(self.count + 1, self.MaxCount)
        self.stop_alert()
        self.update()
        bus.emit('caseCollator/count', self.count, True)
    
    def on_press_minus(self):
        self.count = max(self.count - 1, 0)
        self.stop_alert()
        self.update()
        bus.emit('caseCounter/count', self.count, True)
    
    def on_press_reset(self):
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

    def on_press_settings(self):
        self.stop_alert()
        if not self.motorSpeedDialog:
            self.motorSpeedDialog = MotorSpeedDialog()
            self.motorSpeedDialog.title = 'Case Motor'
            self.motorSpeedDialog.slider.bind(value = self.on_motorSpeed_change)
        self.motorSpeedDialog.slider.value = self.motorDutycycle
        self.motorSpeedDialog.open()

    def on_motorSpeed_change(self, inst, value):
        self.motorDutycycle = value
        if self.running:
            pi.set_PWM_dutycycle(self.motorPort, self.motorDutycycle)
        
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
        
