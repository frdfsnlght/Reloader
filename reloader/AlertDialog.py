
import pigpio

from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup

from .bus import bus
from .gpio import pi
from .Config import Config


Builder.load_string('''
<AlertDialog>:
    alerts: ''

    title: 'Alert'
    title_size: '20sp'
    size_hint: 0.6, None
    height: '375sp'
    
    BoxLayout:
        orientation: 'vertical'
        spacing: '10sp'
        padding: '10sp'
        Label:
            id: textLabel
            font_size: '20sp'
            halign: 'center'
            text: self.parent.parent.parent.parent.alerts
            height: self.text_size[1] if self.text_size[1] else 0
        BoxLayout:
            orientation: 'horizontal'
            Label:
            ImageButton:
                image_normal: 'mute_normal.png'
                image_down: 'mute_down.png'
                size_hint: None, None
                width: '150sp'
                height: '150sp'
                on_press: self.parent.parent.parent.parent.parent.dismiss()
            Label
''')

class AlertDialog(Popup):

    DutyCycle = 50

    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = AlertDialog()
        return cls._instance
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = Config.config()
        self.buzzerFrequency = 0
        self.buzzerPort = config.getint('core', 'buzzerPort')
        self.buzzerFrequencies = [int(f) for f in config.get('core', 'buzzerFrequencies').split(',')]
        self.buzzerInterval = config.getfloat('core', 'buzzerFrequencyInterval')
        self.buzzerIntervalTimer = Clock.schedule_interval(self.on_change_frequency, self.buzzerInterval)
        bus.add_event(self.on_dismiss, 'reset')
        bus.add_event(self.on_dismiss, 'app/start')
        
        pi.set_mode(self.buzzerPort, pigpio.OUTPUT)
        pi.set_PWM_range(self.buzzerPort, 100)
        pi.set_PWM_dutycycle(self.buzzerPort, 0)
        
        self.buzz()
        
        self.open()
        
    def on_dismiss(self):
        pi.set_PWM_dutycycle(self.buzzerPort, 0)
        self.buzzerIntervalTimer.cancel()
        AlertDialog._instance = None

    def on_change_frequency(self, dt):
        self.buzzerFrequency = (self.buzzerFrequency + 1) % len(self.buzzerFrequencies)
        self.buzz()
        
    def buzz(self):
        pi.set_PWM_frequency(self.buzzerPort, self.buzzerFrequencies[self.buzzerFrequency])
        pi.set_PWM_dutycycle(self.buzzerPort, self.DutyCycle)
