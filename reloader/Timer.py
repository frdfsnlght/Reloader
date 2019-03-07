
import logging, datetime

from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread

from reloader.bus import bus
from reloader.MultiImageButton import MultiImageButton
from reloader.ImageButton import ImageButton
from reloader.ConfirmDialog import ConfirmDialog


KV = '''
<Timer>:
    timeStr: ''
    running: False
    playPauseImage: 0
    
    orientation: 'horizontal'
    spacing: self.height * 0.06
    Label:
        text: self.parent.timeStr
        text_size: self.size
        font_size: self.height * 0.9
        halign: 'right'
        max_lines: 1
#        padding_y: self.height * 0.15
    GridLayout:
        size_hint_x: None
        width: self.parent.height / 2
        cols: 1
        MultiImageButton:
            images_normal: 'play_normal.png', 'pause_normal.png'
            images_down: 'play_down.png', 'pause_down.png'
            image_set: self.parent.parent.playPauseImage
            on_press: self.parent.parent.on_press_playPause()
            on_release: self.parent.parent.on_release_playPause()
        ImageButton:
            image_normal: 'reset_normal.png'
            image_down: 'reset_down.png'
            on_press: self.parent.parent.on_press_reset()
'''

        
class Timer(BoxLayout):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.running = False
        self.time = 0
        self.resetConfirmDialog = None
        
        self.event = Clock.schedule_interval(self.on_tick, 0.2)
        
        bus.add_event(self.on_outputCounter_count, 'outputCounter/count')
        
        self.update()
        bus.emit('timer/time', self.time)

    def on_tick(self, delta):
        if not self.running: return
        self.time = self.time + delta
        self.update()
        bus.emit('timer/time', self.time)
        
    def on_press_playPause(self):
        self.running = not self.running
    
    def on_release_playPause(self):
        self.update()
    
    def on_press_reset(self):
        if self.time == 0: return
        if not self.resetConfirmDialog:
            self.resetConfirmDialog = ConfirmDialog()
            self.resetConfirmDialog.text = 'Are you sure you want to reset the timer?'
            self.resetConfirmDialog.bind(on_dismiss = self.on_dismiss_reset)
        self.resetConfirmDialog.open()
    
    def on_dismiss_reset(self, inst):
        if inst.confirmed:
            self.running = False
            self.time = 0
            self.update()
            bus.emit('timer/time', self.time)
    
    #@bus.on('outputCounter/count')
    def on_outputCounter_count(self, count, manual):
        if not manual and not self.running:
            self.running = True
            self.update()
    
    @mainthread
    def update(self):
        self.playPauseImage = 1 if self.running else 0
        self.timeStr = str(datetime.timedelta(seconds = int(self.time)))
        
