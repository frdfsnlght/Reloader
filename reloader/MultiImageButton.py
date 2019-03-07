
from kivy.lang.builder import Builder

from .ImageButton import ImageButton


KV = '''
<MultiImageButton>:
    images_normal: '', ''
    images_down: '', ''
    image_set: 0
    image_normal: self.images_normal[self.image_set]
    image_down: self.images_down[self.image_set]
'''

class MultiImageButton(ImageButton):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
