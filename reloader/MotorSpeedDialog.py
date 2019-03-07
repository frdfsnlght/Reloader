
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


KV = '''
<MotorSpeedDialog>:
    slider: slider
    title_size: '20sp'
    
    size_hint: 0.6, 0.8
    BoxLayout:
        orientation: 'vertical'
        spacing: '10sp'
        padding: '10sp'
        Slider:
            id: slider
            min: 0
            max: 100
            step: 1
            orientation: 'vertical'
        Label:
            size_hint_y: 0.1
            text: str(int(slider.value)) + '%'
            text_size: self.size
            font_size: self.height
            line_height: 0
            halign: 'center'
'''

class MotorSpeedDialog(Popup):

    slider = ObjectProperty()
    
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
