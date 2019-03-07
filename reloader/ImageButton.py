
from kivy.lang.builder import Builder
from kivy.uix.button import Button


KV = '''
<ImageButton>:
    image_normal: ''
    image_down: ''
    background_color: 0, 0, 0, 0
    padding: self.width * 0.05, self.height * 0.05
    Image:
        source: self.parent.image_normal
        allow_stretch: True
        center: self.parent.center
        width: self.parent.width - (self.parent.padding_x * 2) if self.parent.state == 'normal' else 0
        height: self.parent.height - (self.parent.padding_y * 2)
    Image:
        source: self.parent.image_down
        allow_stretch: True
        center: self.parent.center_x - ((self.parent.width - (self.parent.padding_x * 2)) / 2), self.parent.center_y
        width: (self.parent.width - (self.parent.padding_x * 2)) if self.parent.state == 'down' else 0
        height: self.parent.height - (self.parent.padding_y * 2)
'''

# Is this a bug? Notice the 'center' property of the second image. Why is the parent's center shifted in the down state?

class ImageButton(Button):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)

        