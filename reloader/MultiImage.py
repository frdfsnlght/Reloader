
from kivy.lang.builder import Builder
from kivy.uix.label import Label


Builder.load_string('''
<MultiImage>:
    images: '', ''
    image_idx: 0
    padding: self.width * 0.05, self.height * 0.05
    Image:
        source: self.parent.images[self.parent.image_idx]
        allow_stretch: True
        center: self.parent.center
        width: self.parent.width - (self.parent.padding_x * 2)
''')

class MultiImage(Label):    # inherit from label because it has 'padding'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
