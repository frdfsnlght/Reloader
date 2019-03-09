
from kivy.lang.builder import Builder
from kivy.uix.label import Label


KV = '''
<MultiImage>:
    images: '', ''
    image_idx: 0
    padding: self.width * 0.05, self.height * 0.05
    Image:
        source: self.parent.images[self.parent.image_idx]
        allow_stretch: True
        center: self.parent.center
        width: self.parent.width - (self.parent.padding_x * 2)
'''

class MultiImage(Label):    # inherit from label because it had 'padding'

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
