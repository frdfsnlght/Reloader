
from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView


Builder.load_string('''
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
''')

class ConfirmDialog(ModalView):

    def __init__(self, text, on_confirm, on_cancel = None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._on_confirm = on_confirm
        self._on_cancel = on_cancel
        self.open()

    def on_press_confirm(self):
        self.dismiss()
        if self._on_confirm:
            self._on_confirm(self)
            
    def on_press_cancel(self):
        self.dismiss()
        if self._on_cancel:
            self._on_cancel(self)
