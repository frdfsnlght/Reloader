
from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView


KV = '''
<ConfirmDialog>:
    auto_dismiss: False
    text: ''
    confirm_text: 'Yes'
    cancel_text: 'No'
    
    size_hint: 0.9, None
    height: '200sp'
    padding: '10sp'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10sp'
        Label:
            text: self.parent.parent.text
            text_size: self.size
            font_size: '20sp'
            halign: 'center'
            valign: 'middle'
        BoxLayout:
            size_hint_y: None
            height: '80sp'
            orientation: 'horizontal'
            spacing: '10sp'
            padding: '10sp'
            Label:
            Button:
                text: self.parent.parent.parent.confirm_text
                on_press: self.parent.parent.parent.on_press_confirm()
            Button:
                text: self.parent.parent.parent.cancel_text
                on_press: self.parent.parent.parent.on_press_cancel()
            Label:
'''

class ConfirmDialog(ModalView):

    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ConfirmDialog()
        return cls._instance
        
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.confirmed = False
        self.canceled = False

    def on_press_confirm(self):
        self.confirmed = True
        self.canceled = False
        self.dismiss()
            
    def on_press_cancel(self):
        self.confirmed = False
        self.canceled = True
        self.dismiss()
