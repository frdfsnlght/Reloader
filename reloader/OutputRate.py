
import logging

from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import mainthread

from reloader.bus import bus


KV = '''
<OutputRate>:
    rateStr: ''
    
    BackgroundLabel:
        text: 'Output Rate'
        
    BoxLayout:
        orientation: 'horizontal'
        spacing: self.height * 0.06
        Label:
            text: self.parent.parent.rateStr
            text_size: self.size
            font_size: self.height * 0.9
            halign: 'right'
            max_lines: 1
            padding_y: self.height * 0.15
'''

class OutputRate(RelativeLayout):

    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.time = 0
        self.count = 10
        
        bus.add_event(self.on_timer_time, 'timer/time')
        bus.add_event(self.on_outputCounter_count, 'outputCounter/count')
        
        self.update()

    #@bus.on('timer/time')
    def on_timer_time(self, time = 0):
        self.time = time
        self.update()
        
    #@bus.on('outputCounter/count')
    def on_outputCounter_count(self, count, manual):
        self.count = count
        self.update()
        
    @mainthread
    def update(self):
        if self.time > 0:
            self.rateStr = str(int(self.count / (self.time / 3600)))
        else:
            self.rateStr = '---'
        