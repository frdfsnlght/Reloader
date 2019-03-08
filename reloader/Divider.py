
from kivy.lang.builder import Builder
from kivy.uix.label import Label


KV = '''
<Divider>:
    height: '1sp'
    size_hint_y: None
    color: (0.5, 0.5, 0.5, 1)
    canvas.before:
        Color:
            rgba: self.color
        Rectangle:
            pos: self.pos
            size: self.size
'''


class Divider(Label):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        