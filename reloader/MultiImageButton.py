
from kivy.lang.builder import Builder

from .ImageButton import ImageButton


Builder.load_string('''
<MultiImageButton>:
    images_normal: '', ''
    images_down: '', ''
    image_set: 0
    image_normal: self.images_normal[self.image_set]
    image_down: self.images_down[self.image_set]
''')

class MultiImageButton(ImageButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
