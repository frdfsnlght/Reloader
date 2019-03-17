
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.clock import Clock


Builder.load_string('''
<ImageButton>:
    image_normal: ''
    image_down: ''
    
    background_color: 0, 0, 0, 0
    padding: self.width * 0.05, self.height * 0.05
    
#    canvas.after:
#        Color:
#            rgba: 1, 1, 0, 1
#        Line:
#            width: 1
#            rectangle: self.x, self.y, self.width - 1, self.height - 1
    
    Image:
        source: self.parent.image_normal
        allow_stretch: True
        center: self.parent.center
        width: self.parent.width - (self.parent.padding_x * 2) if self.parent.state == 'normal' else 0
    Image:
        source: self.parent.image_down
        allow_stretch: True
        center: self.parent.center_x - ((self.parent.width - (self.parent.padding_x * 2)) / 2), self.parent.center_y
        width: (self.parent.width - (self.parent.padding_x * 2)) if self.parent.state == 'down' else 0
''')

# Is this a bug? Notice the 'center' property of the second image. Why is the parent's center shifted in the down state?

class ImageButton(Button):

    long_press_delay = NumericProperty(1)
    long_press_interval = NumericProperty(0.2)
    
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
    