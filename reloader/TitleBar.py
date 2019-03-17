
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

from .bus import bus
from .ImageButton import ImageButton
from .ConfirmDialog import ConfirmDialog
from .PowerDialog import PowerDialog


Builder.load_string('''
<TitleBar>:
    orientation: 'horizontal'
    padding: '5sp'
    
#    canvas.before:
#        Color:
#            rgba: 1, 1, 1, 1
#        Line:
#            width: 1
#            points: self.x, self.y, self.x + self.width, self.y
            
    Label:
        text: 'Reloader'
        text_size: self.size
        font_size: self.height * 0.8
        halign: 'left'
        valign: 'middle'
        max_lines: 1
        color: 0.9, 0.9, 0.9, 1
        padding_y: self.height * 0.15
    ImageButton:
        image_normal: 'reset_normal.png'
        image_down: 'reset_down.png'
        size_hint_x: None
        width: self.height
        on_press: self.parent.on_press_reset()
    ImageButton:
        image_normal: 'power_normal.png'
        image_down: 'power_down.png'
        size_hint_x: None
        width: self.height
        on_press: self.parent.on_press_power()
''')

class TitleBar(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press_reset(self):
        ConfirmDialog(text = 'Are you sure you want to reset everything?', on_confirm = self.on_reset)
    
    def on_reset(self, *args):
        bus.emit('reset')
            
    def on_press_power(self):
        PowerDialog()
