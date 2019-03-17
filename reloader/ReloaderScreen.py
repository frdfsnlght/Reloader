
import logging

from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

from .bus import bus
from .TitleBar import TitleBar
from .Timer import Timer
from .Divider import Divider
from .OutputRate import OutputRate
from .CaseCollator import CaseCollator
from .BulletCollator import BulletCollator
from .OutputCounter import OutputCounter
from .PrimerSensor import PrimerSensor
from .PowderSensor import PowderSensor
from .AlertDialog import AlertDialog


Builder.load_string('''
<ReloaderScreen>:
    cols: 1
    TitleBar:
        height: '70sp'
        size_hint_y: None
    Divider:
    Timer:
        height: '110sp'
        size_hint_y: None
    OutputRate:
        height: '130sp'
        size_hint_y: None
    CaseCollator:
        height: '130sp'
        size_hint_y: None
    BulletCollator:
        height: '130sp'
        size_hint_y: None
    GridLayout:
        cols: 2
#        height: '80sp'
#        size_hint_y: None
        PrimerSensor:
        PowderSensor:
    OutputCounter:
        height: '130sp'
        size_hint_y: None
    
''')

class ReloaderScreen(GridLayout):

    _screen = None
    
    @classmethod
    def screen(cls):
        if not cls._screen:
            cls._screen = ReloaderScreen()
        return cls._screen
        
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.alerts = []
        
        bus.add_event(self.on_caseCollator_empty, 'caseCollator/empty')
        bus.add_event(self.on_caseCollator_clear, 'caseCollator/clear')
        bus.add_event(self.on_bulletCollator_empty, 'bulletCollator/empty')
        bus.add_event(self.on_bulletCollator_clear, 'bulletCollator/clear')
        bus.add_event(self.on_primer_set, 'primerSensor/set')
        bus.add_event(self.on_primer_clear, 'primerSensor/clear')
        bus.add_event(self.on_powder_set, 'powderSensor/set')
        bus.add_event(self.on_powder_clear, 'powderSensor/clear')
        
        bus.add_event(self.hideAlerts, 'reset')
        
        
    def on_caseCollator_empty(self):
        self.addAlert('Case collator is empty')
        
    def on_caseCollator_clear(self):
        self.removeAlert('Case collator is empty')
        
    def on_bulletCollator_empty(self):
        self.addAlert('Bullet collator is empty')
        
    def on_bulletCollator_clear(self):
        self.removeAlert('Bullet collator is empty')
        
    def on_primer_set(self):
        self.addAlert('Primers are empty')
        
    def on_primer_clear(self):
        self.removeAlert('Primers are empty')
        
    def on_powder_set(self):
        self.addAlert('Powder is empty')
        
    def on_powder_clear(self):
        self.removeAlert('Powder is empty')
        
    def addAlert(self, alert):
        if alert not in self.alerts:
            self.alerts.append(alert)
        if self.alerts:
            self.showAlerts()
            
    def removeAlert(self, alert):
        if alert in self.alerts:
            self.alerts.remove(alert)
        if self.alerts:
            self.showAlerts()
        else:
            self.hideAlerts()

    def showAlerts(self):
        alertDialog = AlertDialog.instance()
        alertDialog.alerts = '\n'.join(self.alerts)
    
    def hideAlerts(self):
        self.alerts = []
        if AlertDialog._instance:
            AlertDialog._instance.dismiss()
        