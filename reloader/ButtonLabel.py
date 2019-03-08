
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior


class ButtonLabel(ButtonBehavior, Label):

    long_press_delay = NumericProperty(1)
    long_press_interval = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_long_press')
        self.longPressTimer = Clock.create_trigger(self._on_long_press, self.long_press_delay)
        self.longPressCount = 0

    def on_press(self):
        self.longPressCount = 0
        self.longPressTimer.timeout = self.long_press_delay
        self.longPressTimer()
        
    def on_release(self):
        self.longPressTimer.cancel()
        
    def on_long_press(self, count):
        pass
        
    def _on_long_press(self, dt):
        self.longPressCount = self.longPressCount + 1
        self.dispatch('on_long_press', self.longPressCount)
        if self.long_press_interval > 0:
            self.longPressTimer.timeout = self.long_press_interval
            self.longPressTimer()
        
        