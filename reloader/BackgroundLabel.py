
from kivy.lang.builder import Builder
from kivy.uix.label import Label


KV = '''
<BackgroundLabel>:
    text_size: self.size
    font_size: self.height * 0.3
    halign: 'left'
    valign: 'middle'
    max_lines: 1
    color: 0.1, 0.1, 0.1, 1
    padding_y: self.height * 0.15
    padding_x: '20sp'
'''

class BackgroundLabel(Label):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)

        