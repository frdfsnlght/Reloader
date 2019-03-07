
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout


KV = '''
<TitleBar>:
    orientation: 'horizontal'
    padding: '5sp'
    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            points: self.x, self.y, self.x + self.width, self.y
            
    Label:
        text: 'Reloader'
        text_size: self.size
        font_size: self.height * 0.8
        halign: 'left'
        valign: 'middle'
        max_lines: 1
        color: 0.9, 0.9, 0.9, 1
        padding_y: self.height * 0.15
'''

class TitleBar(BoxLayout):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)

        